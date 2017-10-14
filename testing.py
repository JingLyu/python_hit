"""BASED MAX_SEQ
N=0:   L[0]
Si =  max( S(i-1)  +L[i],  L[i])
"""


def max_seq(i):  # top to bottom
    if dp[i] != "A":
        return dp[i]
    if i == 0:
        dp[0] = int(L[0])

        return L[0]
    dp[i] = max((max_seq(i - 1) + L[i]), L[i])
    return dp[i]


def max_seq_bt(i):  # bottom to top  ; i is length
    dp[0] = L[0]
    if i == 0:
        return dp[0]
    max_sub_seq = dp[0]
    for j in range(1, i):
        next_sum = dp[j - 1] + L[j]

        if next_sum > L[j]:
            dp[j] = next_sum
            if next_sum > max_sub_seq:
                max_sub_seq = next_sum
        else:
            if L[j] > max_sub_seq:  # all negative ,last one is positive.
                max_sub_seq = L[j]

            dp[j] = L[j]
    return max_sub_seq


t = int(input())
for i in range(t):
    n = int(input())
    L = list(map(int, input().split()))
    # print (L)
    max_L = max(L)
    min_L = min(L)
    # print (max_L,min_L)
    if max_L > 0 and min_L >= 0:  # all positive
        sum_L = sum(L)
        print (sum_L, sum_L)
        # break
    elif max_L <= 0 and min_L < 0:
        print (max_L, max_L)
        # break
    # L=[int(x) for x in input().split()]
    # print (L)
    else:
        # print (L)
        L_len = len(L)
        dp = ["A"] * L_len
        # max_seq(L_len-1)
        max_seq_bt(L_len)
        print (max_seq_bt(L_len), sum([x for x in L if x > 0]))
