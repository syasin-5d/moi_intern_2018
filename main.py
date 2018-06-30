import copy
from itertools import permutations
from numeron import Numeron, Answer

def change_str(string, i , change):
    str_list = list(string)
    str_list[i] = str(change)
    str_changed = "".join(str_list)
    return str_changed

def main(level):
    numeron = Numeron(level)
    answer = Answer("".join([str(i) for i in range(level)]))
    numeron.post_answer(answer)
    answer_before = copy.deepcopy(answer)
    """
    blow 特定パート
    """
    for i in range(numeron.level):
        for ans_i in range(10):
            answer_before.set_used()
            if answer_before.used[ans_i] or answer.what_is_blow[ans_i] or answer.what_is_hit[ans_i]:
                continue
            else:
                answer_before.answer = change_str(answer.answer, i, ans_i)
                numeron.post_answer(answer_before)
                # answerを変えていって、blowsが減った結果、元々使われてた数字がblow対象.
                if answer_before.blows < answer.blows:
                    answer.what_is_blow[int(answer.answer[i])] = True
                    break
                # 逆にanswerを変えていって、blowsが増えた結果、変えた数字がblow対象.
                elif answer_before.blows > answer.blows:
                    answer.what_is_blow[int(answer_before.answer[i])] = True
                    answer.answer = answer_before.answer
                    answer.blows = answer_before.blows
                    break
                # hitsに対しても同様
                elif answer_before.hits < answer.hits:
                    answer.what_is_hit[int(answer.answer[i])] = True
                    break
                elif answer_before.hits > answer.hits:
                    answer.what_is_hit[int(answer_before.answer[i])] = True
                    answer.answer = answer_before.answer
                    answer.hits = answer_before.hits
                    break
        if answer.blows + answer.hits is numeron.level:
            break
    """
    hit 特定パート
    """
    answer_post = copy.deepcopy(answer)
    for ans in permutations(answer.answer):
        answer_post.answer = "".join(ans)
        numeron.post_answer(answer_post)
        if(answer_post.hits is numeron.level):
            break
    print("end")

if __name__ == '__main__':
    main(4)
