from tortoise.skyrim_utils.Utils import check_package

class TtsSettings:

    SYNTH_ENGINE_TORTOISE = 'tortoise'
    SYNTH_ENGINE_EMPTY = 'empty'

    @staticmethod
    def get_settings(entry):
        emotion = entry.get('emotion', 'neutral')
        model_settings = TortoiseModelPresets.get_preset(emotion)
        api_settings = TortoiseApiSettings.get_default()
        text = str(entry.get('text', ''))

        # engine
        if text.strip() == '':
            engine = TtsSettings.SYNTH_ENGINE_EMPTY
        else:
            engine = TtsSettings.SYNTH_ENGINE_TORTOISE

        if emotion in ['neutral']:
            candidates = 2
        elif emotion in ['puzzled',  'surprise', 'frustrated', 'curious', 'confident']:
            candidates = 3
        elif emotion in ['disgust', 'sad', 'fear', 'amused', 'happy']:
            candidates = 4
        elif emotion in ['anger', 'hurt', 'sing']:
            candidates = 5

        tts_settings = {
            'engine': engine,
            'candidates': candidates
        }

        return {
            'model': model_settings,
            'api': api_settings,
            'tts': tts_settings
        }


class TortoiseModelPresets:
    """
    Some COOL presets of settings I found for Tortoise tts experimenting.
    ---- Tortoise Explanation ----

    temperature: Increase this value slightly to make the output more varied and less predictable. This can help add expressiveness.

    length_penalty: Decrease this value to allow for longer, more elaborate expressions which are often characteristic of theatrical performances.

    repetition_penalty: Decrease this value slightly to allow for some repetition which can be a feature of dramatic speech.

    top_p: Increase this value to include more tokens in the cumulative probability mass, which can help in creating more varied and expressive speech.

    cond_free_k: Increase this value to make the speech more influenced by the given conditions, enhancing the dramatic effect.

    diffusion_temperature: Increase this value to add more randomness and variability to the diffusion process, which can enhance expressiveness.

    ---- ChatGPT Tutorial ----
    # Temperature:

    * Purpose: Controls the randomness of predictions by scaling the logits before applying softmax.
    * Effect: A higher temperature results in more random outputs, while a lower temperature results in more deterministic outputs.
    * Typical Range: 0.0 to 1.0 (values >1.0 are less common).

    # Length Penalty:

    * Purpose: Adjusts the preference for longer or shorter sequences during generation.
    * Effect: Higher values penalize longer sequences, promoting shorter outputs. Lower values can encourage longer outputs.
    * Typical Range: >0 (values around 1.0 are common).

    # Repetition Penalty:

    * Purpose: Penalizes repeating the same word/phrase.
    * Effect: Higher values reduce the likelihood of repeating the same tokens, promoting diversity in output.
    * Typical Range: >1 (commonly around 1.2 to 2.0).

    # Top-p (Nucleus Sampling):

    * Purpose: Filters out the least likely tokens, keeping only the top p cumulative probability mass.
    * Effect: Controls the trade-off between diversity and quality of generated text. Lower values result in more conservative, higher-quality text, while higher values allow for more diversity.
    * Typical Range: 0.0 to 1.0 (values like 0.8 or 0.9 are common).

    # Cond Free K (Conditional Free k):

    * Purpose: Specific to models that allow controlling for certain conditions or features.
    * Effect: Adjusts how much the condition influences the generation.
    * Typical Range: Varies based on implementation.

    # Diffusion Temperature:

    * Purpose: Similar to temperature in standard generation but specific to models using a diffusion process for generation.
    * Effect: Controls the randomness of the diffusion process, affecting the smoothness or variability of the generated output.
    * Typical Range: Varies based on implementation.
    """

    default = {
        'temperature': .8,
        'length_penalty': 1.0,
        'repetition_penalty': 2.0,
        'top_p': .8,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    high_expressiveness = {
        'temperature': 1.0,
        'length_penalty': 0.8,
        'repetition_penalty': 1.5,
        'top_p': .8,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    top_p_expressive = {
        'temperature': .8,
        'length_penalty': 1.0,
        'repetition_penalty': 2.0,
        'top_p': 0.95,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # sad: Higher repetition penalty for more repetition, lower temperature.
    sad = {
        'temperature': .7,
        'length_penalty': 1.0,
        'repetition_penalty': 2.5,
        'top_p': .85,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # anger: Uses the top_p_expressive() preset with slight modifications.
    angry = {
        'temperature': .9,
        'length_penalty': 1.0,
        'repetition_penalty': 1.8,
        'top_p': 0.95,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # happy: Slightly higher temperature and lower repetition penalty for expressiveness.
    happy = {
        'temperature': .85,
        'length_penalty': 0.9,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # disgust: Similar to neutral but with slight modifications.
    disgust = {
        'temperature': .75,
        'length_penalty': 1.1,
        'repetition_penalty': 2.0,
        'top_p': .85,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # puzzled: Higher temperature for more variability.
    puzzled = {
        'temperature': .9,
        'length_penalty': 1.2,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # fear: High temperature and condition-free to enhance dramatic effect.
    fear = {
        'temperature': 1.0,
        'length_penalty': 0.8,
        'repetition_penalty': 1.5,
        'top_p': .8,
        'cond_free_k': 2.5,
        'diffusion_temperature': 1.0
    }
    # hurt: Similar to sad but slightly different parameters.
    hurt = {
        'temperature': .7,
        'length_penalty': 1.0,
        'repetition_penalty': 2.5,
        'top_p': .85,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # surprise: High temperature for variability and expressiveness.
    surprise = {
        'temperature': .95,
        'length_penalty': 0.9,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # sing: Higher temperature and lower length penalty for more fluidity.
    sing = {
        'temperature': 1.0,
        'length_penalty': 0.8,
        'repetition_penalty': 1.5,
        'top_p': .95,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # confident: Balanced parameters for a confident tone.
    confident = {
        'temperature': .85,
        'length_penalty': 1.0,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # curious: Higher temperature and length penalty for variability.
    curious = {
        'temperature': .9,
        'length_penalty': 1.1,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # frustrated: Balanced but with higher repetition penalty.
    frustrated = {
        'temperature': .9,
        'length_penalty': 1.0,
        'repetition_penalty': 2.0,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }
    # amused: Similar to happy but slightly different parameters.
    amused = {
        'temperature': .9,
        'length_penalty': 1.0,
        'repetition_penalty': 1.5,
        'top_p': .9,
        'cond_free_k': 2.0,
        'diffusion_temperature': 1.0
    }

    @staticmethod
    def get_preset(emotion: str):
        presets = {
            'neutral': TortoiseModelPresets.default,
            'anger': TortoiseModelPresets.angry,
            'happy': TortoiseModelPresets.happy,
            'disgust': TortoiseModelPresets.disgust,
            'puzzled': TortoiseModelPresets.puzzled,
            'sad': TortoiseModelPresets.sad,
            'fear': TortoiseModelPresets.fear,
            'hurt': TortoiseModelPresets.hurt,
            'surprise': TortoiseModelPresets.surprise,
            'sing': TortoiseModelPresets.sing,
            'confident': TortoiseModelPresets.confident,
            'curious': TortoiseModelPresets.curious,
            'frustrated': TortoiseModelPresets.frustrated,
            'amused': TortoiseModelPresets.amused
        }

        return presets.get(emotion, TortoiseModelPresets.default)


class TortoiseApiSettings:

    @staticmethod
    def get_default():
        use_deepspeed = check_package("deepspeed")
        if not use_deepspeed:
            print("WARNING: DeepSpeed is not available. Even though it is not mandatory, the performance will be affected.")
            print("To install on Windows, follow the procedure at docs/tortoise-ttsdeepspeed-instalation-windows.md")

        default = {
            "use_deepspeed": use_deepspeed,
            "kv_cache": True,
            "half": True,
            "produce_debug_state": False,
            "seed": None,
            "cvvp_amount": 0,
            'preset': 'slow',
        }

        return default



