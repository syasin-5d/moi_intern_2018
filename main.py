import copy
from numeron import Numeron, Answer

def main(level):
    numeron = Numeron(level)
    answer = Answer("".join([str(i) for i in range(level)]))
    numeron.post_answer(answer)
    answer_before = copy.deepcopy(answer)
    """
    blow 特定パート
    """
    while(answer.blows + answer.hits is not numeron.level):
        for i in range(numeron.level):
            for ans_i in range(10):
                answer_before.set_used()
                if answer_before.used[ans_i] or answer.what_is_blow[ans_i] or answer.what_is_hit[i]:
                    continue
                else:
                    answer_before.answer = change_str(answer.answer, i, ans_i)
                    numeron.post_answer(answer_before)
                    # hitsに対しても同様
                    if answer_before.hits < answer.hits:
                        answer.what_is_hit[i] = True
                        answer_before.answer = answer.answer
                        break
                    elif answer_before.hits > answer.hits:
                        answer.what_is_hit[i] = True
                        answer.answer = answer_before.answer
                        answer.hits = answer_before.hits
                        break
                    # answerを変えていって、blowsが減った結果、元々使われてた数字がblow対象.
                    elif answer_before.blows < answer.blows:
                        answer.what_is_blow[int(answer.answer[i])] = True
                        answer_before.answer = answer.answer
                        break
                    # 逆にanswerを変えていって、blowsが増えた結果、変えた数字がblow対象.
                    elif answer_before.blows > answer.blows:
                        answer.what_is_blow[int(answer_before.answer[i])] = True
                        answer.answer = answer_before.answer
                        answer.blows = answer_before.blows
                        break
            if answer.blows + answer.hits is numeron.level:
                break
    print("end of blows")

    """
    hit 特定パート
    """
    answer_post = copy.deepcopy(answer)

    while(1):
        # i桁目とj桁目を交換していく
        for i in range(numeron.level):
            # 確定したi桁目は除外
            if answer.what_is_hit[i]:
                continue
            for j in range(i+1,numeron.level):
                # 確定したj桁目は除外
                if answer.what_is_hit[j]:
                    continue
                else:
                    answer_post.answer = swap_str(answer.answer, i, j)
                    numeron.post_answer(answer_post)
                    # 交換した結果, hitsが2増えたとき、確定
                    if answer_post.hits - answer.hits is 2:
                        answer.what_is_hit[i] = True
                        answer.what_is_hit[j] = True
                        answer.answer = answer_post.answer
                        answer.hits = answer_post.hits
                        break
                    # hitsが1増えたとき、交換した2つの数字のうちどっちがhitかわからない
                    elif answer_post.hits - answer.hits is 1:
                        answer.answer = answer_post.answer
                        answer.hits = answer_post.hits
                        break            
    print("end")
        
def change_str(string, i , change):
    str_list = list(string)
    str_list[i] = str(change)
    str_changed = "".join(str_list)
    return str_changed

def swap_str(string, i, j):
    string_1 = change_str(string, i, string[j])
    return change_str(string_1, j, string[i])        

if __name__ == '__main__':
    main(10)
