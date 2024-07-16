"""
Fluxo do zero:
importar dialogos
? realizar customizações no arquivo de import
criar batch
realizar leitura linha a linha do arquivo de batch, e gear audio com parametros customizados
    - o cache to tortoisetts seve ser gerado no diretorio cache
    - baseando-se na emoção os parâmetrso devem ser escolhidos
    - estudar se é possivel salvar estado

Ao executar o tortoise
    - verificar se existe algum estado de modelo salvo
        - se sim, finalizar
        - continuar batch em andamento se existir
    - verificar se existe um batch em andamento
        - continuar batch
    - se nada estiver em andamento, seguir fluxo inicial
"""

import os
import argparse
import sys

from skyrim_utils.BatchBuilder import BatchBuilder
from skyrim_utils.BatchBuilder import STATE_COMPLETED_TRUE
from skyrim_utils.BatchBuilder import STATE_COMPLETED_FALSE
from skyrim_utils.BatchBuilder import STATE_COMPLETED_ONGOING
from skyrim_utils.BatchBuilder import STATE_COMPLETED_ERROR


VERSION = "1.0.0"
RET_ERROR = 1
RET_SUCCESS = 0


import argparse


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
            # todo Solid here
            import_file = os.path.join(BatchBuilder.CACHE_DIR, BatchBuilder.IMPORT_FILE)
            print("Creating batch file...")
            BatchBuilder.create_tts_batch(import_file)
    else:
        print("Batch file already created.")

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
                batchfile = os.path.join(BatchBuilder.CACHE_DIR, BatchBuilder.BATCH_FILE)
                print(f"Use --archive-batch option to archive the active batch, or rename/edit the file {batchfile} manually to proceed.")
            return RET_SUCCESS

        BatchBuilder.update_batch_line(entry["id"], STATE_COMPLETED_ONGOING)
        state = tortoise_do_tts(entry)
        BatchBuilder.update_batch_line(entry["id"], state)


def tortoise_do_tts(entry):
    print("TODO")
    # utilizar a API do tortoise aqui!!
    return STATE_COMPLETED_ERROR


if __name__ == '__main__':
    main()





