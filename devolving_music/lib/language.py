def fuzzy_match(s1: str, s2: str) -> bool:
    s1 = s1.lower()
    s2 = s2.lower()

    overlap_length = min(len(s1), len(s2)) // 2 + 2

    for i in range(len(s1) - overlap_length + 1):
        for j in range(len(s2) - overlap_length + 1):
            print(s1[i:i + overlap_length], s2[j:j + overlap_length])
            if s1[i:i + overlap_length] == s2[j:j + overlap_length]:
                return True

    return False
