import datetime

def TIME():
    return datetime.datetime.now()
def TIMER(total):
    s = total.total_seconds()
    # Returns a string formatted as 0:22.59s
    return f"{int(s // 60):02d}:{(s % 60):.2f}s"
def TIMESTAMP(): #TODO: ZASTARELA FUNKCIJA, Deprecate this function
    return datetime.datetime.now().strftime("%d.%m %H:%M::%S")