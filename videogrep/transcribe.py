from vosk import Model, KaldiRecognizer, SetLogLevel
import imageio_ffmpeg
import os
import subprocess
import json
from typing import List, Optional

MAX_CHARS = 36
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")


def transcribe(videofile: str, model_path: Optional[str] = None) -> List[dict]:
    """
    Transcribes a video file using Vosk

    :param videofile str: Video file path
    :param model_path str: Optional vosk model folder
    :rtype List[dict]: A list of timestamps and content
    """

    transcript_file = os.path.splitext(videofile)[0] + ".json"

    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as infile:
            data = json.load(infile)
        return data

    if not os.path.exists(videofile):
        print("Could not find file", videofile)
        return []

    _model_path: str = MODEL_PATH

    if model_path is not None:
        _model_path = model_path

    if not os.path.exists(_model_path):
        print("Could not find model folder")
        exit(1)

    print("Transcribing", videofile)
    SetLogLevel(-1)

    sample_rate = 16000
    model = Model(_model_path)
    rec = KaldiRecognizer(model, sample_rate)
    rec.SetWords(True)

    process = subprocess.Popen(
        [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-nostdin",
            "-loglevel",
            "quiet",
            "-i",
            videofile,
            "-ar",
            str(sample_rate),
            "-ac",
            "1",
            "-f",
            "s16le",
            "-",
        ],
        stdout=subprocess.PIPE,
    )

    tot_samples = 0
    result = []
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            tot_samples += len(data)
            result.append(json.loads(rec.Result()))
    result.append(json.loads(rec.FinalResult()))

    out = []
    for r in result:
        if "result" not in r:
            continue
        words = [w for w in r["result"]]
        item = {"content": "", "start": None, "end": None, "words": []}
        for w in words:
            item["content"] += w["word"] + " "
            item["words"].append(w)
            if len(item["content"]) > MAX_CHARS or w == words[-1]:
                item["content"] = item["content"].strip()
                item["start"] = item["words"][0]["start"]
                item["end"] = item["words"][-1]["end"]
                out.append(item)
                item = {"content": "", "start": None, "end": None, "words": []}

    if len(out) == 0:
        print("No words found in", videofile)
        return []

    with open(transcript_file, "w", encoding="utf-8") as outfile:
        json.dump(out, outfile)

    from . import srtfile
    transcript_file_srt = os.path.splitext(videofile)[0] + ".srt"
    with open(transcript_file_srt, "w", encoding="utf-8") as outfile:
        outfile.write(srtfile.from_list(out))

    return out
