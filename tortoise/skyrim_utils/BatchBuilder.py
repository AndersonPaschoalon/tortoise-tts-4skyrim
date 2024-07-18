import os
import re
import glob
import traceback
import pandas as pd
from io import StringIO
from datetime import datetime
from tortoise.skyrim_utils.CustomExceptions import *

# == states of the column completed ==
# already completed
STATE_COMPLETED_TRUE = "true"
# not started
STATE_COMPLETED_FALSE = "false"
# in-progress
STATE_COMPLETED_ONGOING = "ongoing"
# error, and cannot be executed
STATE_COMPLETED_ERROR = "error"


class BatchBuilder:
    """
    The purpose if this class is to import from Skyrim root directory all dialogs exported by Creation Kit as
    dialogueExport*.txt files, and create a batch file to be consumed by tortoisetts framework.
    TODO: create pre-batch where i can change the emotions manually
    """
    CACHE_DIR = "cache"
    RESULTS_DIR = "results"
    IMPORT_FILE = os.path.join("import", "import.csv")
    BATCH_FILE = os.path.join("batch", "batch.csv")
    VALID_EMOTIONS = ['neutral', 'anger', 'happy', 'disgust', 'puzzled', 'sad', 'fear', 'hurt', 'surprise', 'sing',
                      'confident', 'curious', 'frustrated', 'amused']
    INPUT_COLUMNS = ['quest', 'voice_type', 'emotion', 'intensity', 'text', 'file', 'filepath', 'source']
    BATCH_HEADER = ['id', 'quest', 'completed', 'voice', 'emotion','text', 'output_path']
    LOW_EMOTION_PREFIXES = {
        "neutral": "",
        "anger": "I'M ANGRY",
        "happy": "I'M HAPPY",
        "disgust": "THIS IS DISGUSTING",
        "puzzled": "I'M PUZZLED",
        "sad": "I'M SAD",
        "fear": "I'M SCARED",
        "hurt": "I'M WOUNDED",
        "surprise": "I'M SURPRISED",
        "sing": "I'M SINGING",
        "confident": "I'M CONFIDENT",
        "curious": "I'M CURIOUS",
        "frustrated": "I'M FRUSTRATED",
        "amused": "I'M AMUSED"
    }
    HIGH_EMOTION_PREFIXES = {
        "neutral": "I'M SERIOUS",
        "anger": "I'M FURIOUS",
        "happy": "I'M ECSTATIC",
        "disgust": "I'M REPULSED",
        "puzzled": "I'M COMPLETELY BAFFLED",
        "sad": "I'M DEVASTATED",
        "fear": "I'M TERRIFIED",
        "hurt": "I'M IN AGONY",
        "surprise": "I'M ASTOUNDED",
        "sing": "I'M SINGING WITH PASSION",
        "confident": "I'M UNSTOPPABLE",
        "curious": "I'M INTENSELY INQUISITIVE",
        "frustrated": "I'M INFURIATED",
        "amused": "I'M ENTHRALLED"
    }
    SKYRIM_EXPORT_DIALOG_PREFIX = "dialogueExport"
    SKYRIM_EXPORT_SCENE_PREFIX = "SceneDialogue"
    SKYRIM_EXPORT_SUFFIX = ".txt"
    EMPTY_VALUE_STR = ""
    EMPTY_VALUE_INT = "0"
    CSV_SEP = ";"

    @staticmethod
    def get_batch_file_path():
        return os.path.join(BatchBuilder.CACHE_DIR, BatchBuilder.BATCH_FILE)

    @staticmethod
    def get_import_file_path():
        return os.path.join(BatchBuilder.CACHE_DIR, BatchBuilder.IMPORT_FILE)

    @staticmethod
    def import_dialogs(skyrim_root):
        BatchBuilder._initialize()
        import_file = BatchBuilder.get_import_file_path()
        df = BatchBuilder._import_all_dialogues(skyrim_root)
        df.to_csv(import_file, sep=BatchBuilder.CSV_SEP, index=False)
        return import_file

    @staticmethod
    def create_tts_batch(import_file):
        df = pd.read_csv(import_file, sep=BatchBuilder.CSV_SEP, dtype=str, header=0, index_col=False)
        try:
            batch_file = BatchBuilder._create_batch_from_dataframe(df, check_voice_samples=False)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    @staticmethod
    def is_batch_active():
        return os.path.exists(BatchBuilder.get_batch_file_path())

    @staticmethod
    def is_import_active():
        return os.path.exists(BatchBuilder.get_import_file_path())

    @staticmethod
    def archive_batch():
        batchfile = BatchBuilder.get_batch_file_path()
        if os.path.exists(batchfile):
            confirmation = input("Are you sure you want to archive the active batch? (Y/N): ").strip().upper()
            if confirmation != 'Y':
                print("Operation canceled.")
                return
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            new_filename = os.path.join(BatchBuilder.CACHE_DIR, f"{BatchBuilder.BATCH_FILE}-{timestamp}.csv")
            os.rename(batchfile, new_filename)
            print(f"Renamed '{batchfile}' to '{new_filename}'")
            print(f"To restore batch, rename {new_filename} to {BatchBuilder.BATCH_FILE} manually.")
        else:
            print("No valid batch to archive")


    @staticmethod
    def archive_import():
        importfile = BatchBuilder.get_import_file_path()
        if os.path.exists(importfile):
            confirmation = input("Are you sure you want to archive the active import? (Y/N): ").strip().upper()
            if confirmation != 'Y':
                print("Operation canceled.")
                return
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
            new_filename = os.path.join(BatchBuilder.CACHE_DIR, f"{BatchBuilder.IMPORT_FILE}-{timestamp}.csv")
            os.rename(importfile, new_filename)
            print(f"Renamed '{importfile}' to '{new_filename}'")
            print(f"To restore batch, rename {new_filename} to {BatchBuilder.IMPORT_FILE} manually.")
        else:
            print("No valid imports to archive.")

    @staticmethod
    def get_next_line(list_completed_states_to_select=None):
        """
        Search the batch.csv from the top to bottom for a line with the column "completed" with the values passed
        as arguments. Default is STATE_COMPLETED_FALSE. It is case insensitive.
        Returns a dict with key equals to the column names.
        Returns None if no line with the provided state exists.
        """
        if list_completed_states_to_select is None:
            list_completed_states_to_select = [STATE_COMPLETED_FALSE, STATE_COMPLETED_ONGOING]

        list_completed_states_to_select = [state.lower() for state in list_completed_states_to_select]

        batch_file_path = BatchBuilder.get_batch_file_path()

        try:
            df = pd.read_csv(batch_file_path, sep=';', dtype=str)
            # Rename the '# id' column to 'id'
            df.rename(columns={'# id': 'id'}, inplace=True)
        except Exception as e:
            print(f"Error reading {batch_file_path}: {e}")
            return None

        for i, row in df.iterrows():
            if row['completed'].strip().lower() in list_completed_states_to_select:
                return row.to_dict()

        return None

    @staticmethod
    def update_batch_line(line_id, new_completed_state: str):
        """
        Update line id to new_completed_state (lower case)
        """
        batch_file_path = BatchBuilder.get_batch_file_path()

        try:
            df = pd.read_csv(batch_file_path, sep=';', dtype=str)
            # Rename the '# id' column to 'id'
            df.rename(columns={'# id': 'id'}, inplace=True)
        except Exception as e:
            print(f"Error reading {batch_file_path}: {e}")
            return False

        if 'id' not in df.columns or 'completed' not in df.columns:
            print("Required columns 'id' and 'completed' are not in the CSV file.")
            return False

        line_id = str(line_id).strip()
        new_completed_state = new_completed_state.lower().strip()

        if line_id not in df['id'].values:
            print(f"Line id {line_id} not found in the batch.")
            return False

        df.loc[df['id'] == line_id, 'completed'] = new_completed_state

        try:
            df.to_csv(batch_file_path, sep=';', index=False)
            return True
        except Exception as e:
            print(f"Error saving {batch_file_path}: {e}")
            return False

    #####################################################

    @staticmethod
    def _import_all_dialogues(skyrim_root):
        """
        Import all the dialogs from skyrim root directories, and transform it in a pandas Dataframe, to be used to
        create the batches.
        """
        list_dialogs = []
        dialog_pattern = os.path.join(skyrim_root,
                                      f"{BatchBuilder.SKYRIM_EXPORT_DIALOG_PREFIX}*{BatchBuilder.SKYRIM_EXPORT_SUFFIX}")
        list_dialogs = glob.glob(dialog_pattern)
        # list_scenes = []
        # scene_pattern = os.path.join(skyrim_root,
        #                             f"{BatchBuilder.SKYRIM_EXPORT_SCENE_PREFIX}*{BatchBuilder.SKYRIM_EXPORT_SUFFIX}")
        # list_scenes = glob.glob(scene_pattern)
        return BatchBuilder._parse_dialogues(list_dialogs)

    @staticmethod
    def _parse_dialogues(list_dialogs):
        loaded_data = []
        for dialog_file in list_dialogs:
            try:
                # df = pd.read_csv(dialog_file, sep='\t', dtype=str, header=0, index_col=False)
                print(f"Loading file {dialog_file}")
                df = BatchBuilder._load_dataframe_helper(dialog_file)
            except Exception as e:
                print(f"Error reading {dialog_file}: {e}")
                traceback.print_exc()
                continue

            for i, row in df.iterrows():
                # Extract and trim the required values
                quest = row['QUEST'].strip() if pd.notna(row['QUEST']) else BatchBuilder.EMPTY_VALUE_STR
                voice_type = row['VOICE TYPE'].strip() if pd.notna(row['VOICE TYPE']) else BatchBuilder.EMPTY_VALUE_STR
                emotion_full = row['EMOTION'].strip() if pd.notna(row['EMOTION']) else f"{BatchBuilder.EMPTY_VALUE_STR} {BatchBuilder.EMPTY_VALUE_INT}"
                emotion, intensity = emotion_full.split(' ')
                text = row['RESPONSE TEXT'].strip().replace(BatchBuilder.CSV_SEP, ",").replace('"', "'")  if pd.notna(row['RESPONSE TEXT']) else BatchBuilder.EMPTY_VALUE_STR
                file = row['FILENAME'].strip() if pd.notna(row['FILENAME']) else BatchBuilder.EMPTY_VALUE_STR
                filepath = row['FULL PATH'].strip() if pd.notna(row['FULL PATH']) else BatchBuilder.EMPTY_VALUE_STR
                source = os.path.basename(dialog_file)

                # Check for empty values and log the error
                for col, value in zip(BatchBuilder.INPUT_COLUMNS[:-1], [quest, voice_type, emotion, intensity, text, file, filepath]):
                    if value == BatchBuilder.EMPTY_VALUE_STR:
                        print(f"WARNING: Cannot recover value '{col}' at line {i + 1} in file {source}. This information might be missing from source file.")

                loaded_data.append([quest, voice_type, emotion, intensity, text, file, filepath, source])

        # Convert the loaded data into a DataFrame
        loaded_df = pd.DataFrame(loaded_data, columns=BatchBuilder.INPUT_COLUMNS)

        # Save the DataFrame to a CSV file, just for debug
        # loaded_df.to_csv('load_test.csv', sep=BatchBuilder.CSV_SEP, index=False)
        return loaded_df

    @staticmethod
    def _initialize():
        # Create the output directory if it doesn't exist
        os.makedirs(BatchBuilder.CACHE_DIR, exist_ok=True)
        os.makedirs(BatchBuilder.RESULTS_DIR, exist_ok=True)

    @staticmethod
    def _create_batch_from_dataframe(df, check_voice_samples=True):
        """
        The purpose of this method is create a batch.csv file responsible to manage the batches of audios to generate.
        """
        batch_data = []
        for i, row in df.iterrows():
            # validate emotion values
            emotion = row['emotion'].strip().lower()
            if emotion not in BatchBuilder.VALID_EMOTIONS:
                raise InvalidEmotionException(
                    f"Line {i + 1}: Invalid emotion '{row['emotion']}'. It must be one of {BatchBuilder.VALID_EMOTIONS}.")

            # validate if the voice sample folder does exist
            voice_type = row['voice_type'].strip().lower()
            if check_voice_samples:
                valid_voice_path = os.path.join('tortoise/voices', voice_type + emotion)
                if not os.path.exists(valid_voice_path):
                    raise InvalidVoiceTypeException(
                        f"Line {i + 1}: Invalid actor_voice_type '{voice_type}' with emotion '{row['emotion']}'. "
                        "It must be a folder inside 'tortoise/voices' or 'tortoise/voices' with the emotion appended.")

            # validate the intendity column
            intensity = 0
            try:
                intensity = int(row['intensity'])
            except ValueError:
                raise InvalidIntensityException(
                    f"Line {i + 1}: intensity must be an integer: {row['intensity']}")

            # validate the text
            text = row['text']
            if pd.isna(text):
                text = BatchBuilder.EMPTY_VALUE_STR
            if not isinstance(text, str):
                raise InvalidTextException(f"Line {i + 1}: actor_text must be a valid string: {text}")

            # validate the path where the results will be saved
            filepath = row['filepath']
            if not isinstance(filepath, str) or not filepath.strip():
                raise InvalidFilePathException(f"Line {i + 1}: filepath must be a valid path: {filepath}")

            # validate the quest id
            quest_id = row['quest']
            if not isinstance(text, str):
                raise InvalidTextException(f"Line {i + 1}: quest must be a valid string: {quest_id}")

            mod_text = BatchBuilder._modify_text_with_emotion(text, emotion, intensity)
            batch_line = [str(i), quest_id, STATE_COMPLETED_FALSE, voice_type + emotion, emotion, mod_text,
                          os.path.join(BatchBuilder.RESULTS_DIR, filepath)]
            batch_data.append(batch_line)

        # Create batch.csv with headers
        batch_file_path = BatchBuilder.get_batch_file_path()
        with open(batch_file_path, 'w') as batch_file:
            batch_file.write("# " + BatchBuilder.CSV_SEP.join(BatchBuilder.BATCH_HEADER) + "\n")
            for line in batch_data:
                batch_file.write(BatchBuilder.CSV_SEP.join(line) + "\n")
        print(f"Batch file created at {batch_file_path}")
        return batch_file_path

    @staticmethod
    def _modify_text_with_emotion(text, emotion, intensity):
        emotion_lower = emotion.strip().lower()
        emotion_prefixes = [BatchBuilder.LOW_EMOTION_PREFIXES.get(emotion_lower, "")]
        if intensity > 60:
            emotion_prefixes.append(BatchBuilder.HIGH_EMOTION_PREFIXES.get(emotion_lower, ""))
        emotion_prefix = ""
        for pref in emotion_prefixes:
            if pref != "":
                emotion_prefix += f"[{pref}]"

                # Use regular expression to split the text while keeping the delimiters
        phrases = re.split(r'([.?!]+)', text.strip())
        modified_phrases = []

        # Iterate over phrases and delimiters in pairs
        for i in range(0, len(phrases) - 1, 2):
            phrase = phrases[i].strip()
            delimiter = phrases[i + 1]
            if phrase != "":
                modified_phrase = f"{emotion_prefix} {phrase}"
                modified_phrases.append(modified_phrase + delimiter)

        # Handle any remaining text without a trailing delimiter
        if (len(phrases) % 2 != 0) and (phrases[-1].strip() != ""):
            modified_phrases.append(f"{emotion_prefix} {phrases[-1].strip()}")

        # Join the modified phrases back together
        modified_text = ' '.join(modified_phrases)
        return modified_text

    @staticmethod
    def _load_dataframe_helper(dialog_file):
        def replace_special_chars(text):
            # Define replacements for common special characters
            replacements = {
                "…": "...",
                "’": "'",
                "‘": "'",
                "“": "\"",
                "”": "\"",
                "–": "-",
                "—": "-",
                "•": "-",
                "•": "-",
                # Add any other replacements as needed
            }

            # Replace characters based on the replacements dictionary
            for char, replacement in replacements.items():
                text = text.replace(char, replacement)

            # Remove any non-ASCII characters
            text = re.sub(r'[^\x00-\x7F]+', '', text)

            return text

        # Read the content of the file and preprocess it in memory
        with open(dialog_file, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
            processed_lines = [replace_special_chars(line) for line in lines]

        # Join the processed lines and load into a DataFrame
        processed_content = ''.join(processed_lines)

        df = pd.read_csv(StringIO(processed_content), sep='\t', dtype=str, header=0, index_col=False)

        return df


def __test__modify_text_with_emotion():
    #
    # TEST modify_text_with_emotion()
    #
    p1 = "Hello! How are you?"
    p2 = "I'm Kratos, the God Of War!"
    p3 = "Look... I'm wounded... I need help! Fast!"
    p4 = "Look... I'm wounded... I need help! Fast!   "
    p5 = "  Test. Test.  "
    p6 = ""
    p7 = "Thas right, I need your help"

    print("-- " + BatchBuilder._modify_text_with_emotion(p1, "Invalid value", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p1, "", 70))
    print("-- " + BatchBuilder._modify_text_with_emotion(p1, "Neutral", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p1, "Neutral", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "Anger", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "Anger", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "happy", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "happy", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "disgust", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "disgust", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "puzzled", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "puzzled", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "sad", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p2, "sad", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p3, "Hurt", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p3, "Hurt", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p4, "Anger", 50))
    print("-- " + BatchBuilder._modify_text_with_emotion(p5, "Anger", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p5, "Anger", 70))
    print("-- " + BatchBuilder._modify_text_with_emotion(p6, "Anger", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p5, "fear", 70))
    print("-- " + BatchBuilder._modify_text_with_emotion(p6, "fear", 70))

    print("-- " + BatchBuilder._modify_text_with_emotion(p7, "happy", 70))


def __test___parse_dialogues():
    BatchBuilder._import_all_dialogues('C:\Program Files (x86)\Steam\steamapps\common\SkyrimBackups\DevDSilHand\Skyrim')


def __test__create_tts_batch():
    import_file = BatchBuilder.import_dialogs('C:\Program Files (x86)\Steam\steamapps\common\SkyrimBackups\DevDSilHand\Skyrim')
    BatchBuilder.create_tts_batch(import_file)


def __test__get_next_batch_line():
    entry = BatchBuilder.get_next_line()
    print(entry)


def __test_update_line_batch():
    updated = BatchBuilder.update_batch_line(3, STATE_COMPLETED_TRUE)
    if updated:
        print("Batch line updated successfully.")
    else:
        print("Failed to update batch line.")

    updated = BatchBuilder.update_batch_line(5, STATE_COMPLETED_ERROR)
    if updated:
        print("Batch line updated successfully.")
    else:
        print("Failed to update batch line.")

    updated = BatchBuilder.update_batch_line(7, STATE_COMPLETED_ONGOING)
    if updated:
        print("Batch line updated successfully.")
    else:
        print("Failed to update batch line.")


if __name__ == "__main__":
    test01 = False
    test02 = False
    test03 = False
    test04 = False
    test05 = True

    if test01:
        __test__modify_text_with_emotion()
    if test02:
        __test___parse_dialogues()
    if test03:
        __test__create_tts_batch()
    if test04:
        __test__get_next_batch_line()
    if test05:
        __test_update_line_batch()









