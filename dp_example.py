# Enter your code here. Read input from STDIN. Print output to STDOUT
# Enter your code here. Read input from STDIN. Print output to STDOUT
dp = []
s1, s2 = None, None


def is_solve(n1, n2):
    print n1,n2
    if n1 == -1 and n2 == -1:
        return True
    if n1 == -1:
        return False
    if n2 == -1:
        return (s1[:n1 + 1].lower() == s1[:n1 + 1])

    if dp[n1][n2] != -1: return dp[n1][n2]

    sol = (is_solve(n1 - 1, n2) and s1[n1].lower() == s1[n1]) or (
    is_solve(n1 - 1, n2 - 1) and s1[n1].lower() == s2[n2].lower())

    print (sol)
    print s1[n1], s2[n2]
    dp[n1][n2] = sol
    # print (dp)
    return sol


s1  ='daBcd'
s2 ='ABC'
dp = [[-1, ] * len(s2) for k in range(len(s1))]
    # print (dp)
print("YES" if is_solve(len(s1) - 1, len(s2) - 1) else "NO")