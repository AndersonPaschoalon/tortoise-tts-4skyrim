import os
import argparse
import torch
import torchaudio
from pathlib import Path
import traceback
import sys

from api import TextToSpeech, MODELS_DIR
from tortoise.skyrim_utils.Utils import create_empty_audio
from utils.audio import load_voices
from skyrim_utils.Logger import LoggingStream
from skyrim_utils.BatchBuilder import BatchBuilder
from skyrim_utils.BatchBuilder import STATE_COMPLETED_FALSE
from skyrim_utils.BatchBuilder import STATE_COMPLETED_TRUE
from skyrim_utils.BatchBuilder import STATE_COMPLETED_ONGOING
from skyrim_utils.BatchBuilder import STATE_COMPLETED_ERROR
from skyrim_utils.Settings import TortoiseApiSettings, TortoiseModelPresets, TtsSettings

VERSION = "1.0.0"
RET_ERROR = 1
RET_SUCCESS = 0
SETTINGS = {
    "use_deepspeed": True,
    "kv_cache": True,
    "half": True,
}

#
def main():
    parser = argparse.ArgumentParser(description='tortoise4skyrim: A tool for generating Skyrim character dialogues using Tortoise TTS.')

    parser.add_argument('--archive-import', '-c', action='store_true', help='Archive active import, if any')
    parser.add_argument('--import-dialogs', '-i', type=str,
                        help='Import exported dialogs from Creation Kit from the specified path')

    parser.add_argument('--archive-batch', '-a', action='store_true', help='Archive active batch, if any')
    parser.add_argument('--batch-generate', '-b', action='store_true',
                        help='Create the batch and start synthesizing the audio generation')

    parser.add_argument('--version', '-v', action='version', version=f'tortoise4skyrim {VERSION}', help='Show version')

    args = parser.parse_args()

    if args.archive_import:
        archive_import()
        sys.exit(RET_SUCCESS)

    if args.archive_batch:
        archive_batch()
        sys.exit(RET_SUCCESS)

    if args.import_dialogs:
        import_dialogs(args.import_dialogs)
        sys.exit(RET_SUCCESS)

    if args.batch_generate:
        ret = batch_generate()
        sys.exit(ret)


def archive_import():
    BatchBuilder.archive_import()


def archive_batch():
    BatchBuilder.archive_batch()


def import_dialogs(path):
    if BatchBuilder.is_import_active():
        print("Import procedure already have been executed.")
        print("To import again the dialogs from CreationKit, use the option --archive-import")
        return
    print(f"Importing exported dialogs from Creation Kit from path: {path}")


def batch_generate():
    # Check if batch is active or not.
    if not BatchBuilder.is_batch_active():
        if not BatchBuilder.is_import_active():
            print("Error: dialogs must be imported from CreationKit before creation batch. Use --help option for help.")
            return RET_ERROR
        else:
            import_file = BatchBuilder.get_import_file_path()
            print("Creating batch file...")
            BatchBuilder.create_tts_batch(import_file)
    else:
        print("Batch file already created.")

    LoggingStream.initialize(log_dir=BatchBuilder.get_log_dir(), log_file="tortoise-tts-4skyrim.log")

    # batch is already active, start batch loop.
    print("Starting batch audio generation...")
    while True:
        entry = BatchBuilder.get_next_line()

        # batch finished
        if entry == None:
            resp = input("No valid batch to proceed. Do you want to archive current batch?(Y/N)").strip().upper()
            if resp == "Y":
               BatchBuilder.archive_batch()
            else:
                # solid here
                batchfile = BatchBuilder.get_batch_file_path()
                print(f"Use --archive-batch option to archive the active batch, or rename/edit the file {batchfile} manually to proceed.")
            break

        BatchBuilder.update_batch_line(entry["id"], STATE_COMPLETED_ONGOING)
        state = tortoise_do_tts(entry)
        BatchBuilder.update_batch_line(entry["id"], state)

    LoggingStream.finalize()
    return RET_SUCCESS


def remove_filename_from_path(file_path):
    path = Path(file_path)
    directory = path.parent
    return str(directory) + os.sep


def tortoise_do_tts(entry, bypass=False):
    if bypass:
        print(f"Skipping speach synthesis for entry {entry}.")
        LoggingStream.finalize()
        return STATE_COMPLETED_TRUE

    try:
        print("\n##########################################################################")
        print(f"Starting Voice Synthesis [{entry['id']}]: {entry['quest']}")
        print("##########################################################################")

        print(f"entry: {entry}")

        model_dir = BatchBuilder.get_models_dir()
        settings = TtsSettings.get_settings(entry)
        preset = settings['model']
        api = settings['api']
        tts = settings['tts']
        candidates = tts['candidates']
        engine = tts['engine']

        output_dir = remove_filename_from_path(entry["output_path"])
        output_file_name, _ = os.path.splitext(os.path.basename(entry["output_path"]))
        print(f"Creating output path {output_dir}...")
        os.makedirs(output_dir, exist_ok=True)

        # I may add more tools for tts later...
        if engine == TtsSettings.SYNTH_ENGINE_EMPTY:
            # empty audio
            create_empty_audio(filename=os.path.join(output_dir, f'{output_file_name}.wav'), duration=2)
        else:
            # tortoise
            tts = TextToSpeech(models_dir=model_dir, use_deepspeed=api['use_deepspeed'], kv_cache=api['kv_cache'],
                               half=api['half'])

            # voice_samples, conditioning_latents = load_voices(entry['voice'])
            voice_samples, conditioning_latents = load_voices("malenordneutral")

            gen, dbg_state = tts.tts_with_preset(entry['text'], k=candidates, voice_samples=voice_samples,
                                                 conditioning_latents=conditioning_latents,
                                                 preset=api['preset'], use_deterministic_seed=api['seed'],
                                                 return_deterministic_state=True, cvvp_amount=api['cvvp_amount'],
                                                 temperature=preset['temperature'], length_penalty=preset['length_penalty'],
                                                 repetition_penalty=preset['repetition_penalty'], top_p=preset['top_p'],
                                                 cond_free_k=preset['cond_free_k'],
                                                 diffusion_temperature=preset['diffusion_temperature'])
            if isinstance(gen, list):
                for j, g in enumerate(gen):
                    pre_ext = "" if j == 0 else f"_{j}"
                    torchaudio.save(os.path.join(output_dir, f'{output_file_name}{pre_ext}.wav'), g.squeeze(0).cpu(), 24000)
            else:
                torchaudio.save(os.path.join(output_dir, f'{output_file_name}.wav'), gen.squeeze(0).cpu(), 24000)

        return STATE_COMPLETED_TRUE

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return STATE_COMPLETED_ERROR


if __name__ == '__main__':
    main()





