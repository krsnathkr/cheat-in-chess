import pyttsx3
_NUM = {"1":"one","2":"two","3":"three","4":"four",
        "5":"five","6":"six","7":"seven","8":"eight"}
_PROMO = {"q":"queen","r":"rook","b":"bishop","n":"knight"}


def init_tts():
    eng = pyttsx3.init()
    eng.setProperty("rate", eng.getProperty("rate")-30)
    eng.setProperty("volume",1.0)
    return eng

def uci_to_spoken(uci:str)->str:
    if uci in ("e1g1","e8g8"): return "castle king side"
    if uci in ("e1c1","e8c8"): return "castle queen side"
    src,dst,promo = uci[:2],uci[2:4],uci[4:] if len(uci)==5 else ""
    sq = lambda s: f"{s[0].upper()} {_NUM[s[1]]}"
    phrase = f"{sq(src)} to {sq(dst)}"
    if promo: phrase += f", promote to {_PROMO.get(promo,promo)}"
    return phrase

#function to speak the move using tts engine
def speak_move(tts_engine, uci:str):
    if not tts_engine or uci in {"Invalid FEN","Game Over"}: return
    try:
        tts_engine.say(uci_to_spoken(uci))
        tts_engine.runAndWait()
    except Exception as e:
        print("TTS error:",e)
