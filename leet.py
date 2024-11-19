array = [1,1,1,7,8,9]
k = 3

class Solution:
    def maximumSubarraySum(self, array, k):
        m = 0
        for i in range(len(array) - k + 1):
            sar = array[i:i+k]
            print(sar)
            if len(set(sar)) != k:
                continue
            s = sum(sar)
            if s > m:
                m = s
                
        
        return m


print(Solution().maximumSubarraySum(array, k))