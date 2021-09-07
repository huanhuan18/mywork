from typing import List


def binarySearch(nums: List[int], target: int) -> List[int]:
    """34.在排序数组中查找元素的第一个和最后一个位置"""
    """写两个二分查找"""

    def findFirstPosition():
        low = 0
        high = len(nums) - 1
        index = -1
        while low <= high:
            mid = int(low + (high - low) / 2)
            if nums[mid] >= target:
                high = mid - 1  # 尽量往左，所以是mid-1
            else:
                low = mid + 1  # 非得往右，nums[mid]<target
            if nums[mid] == target:
                index = mid
        return index

    def findLastPosition():
        low = 0
        high = len(nums) - 1
        index = -1
        while low <= high:
            mid = int(low + (high - low) / 2)
            if nums[mid] <= target:
                low = mid + 1
            else:
                high = mid - 1
            if nums[mid] == target:
                index = mid
        return index

    return [findFirstPosition(), findLastPosition()]


def combinationSum(nums: List[int], target: int) -> List[List[int]]:
    """39.组合总和"""
    """搜索回溯"""
    res = []

    def helper(res, tmp, nums, target, index):
        if target <= 0:
            if target == 0:
                tmp1 = list(tmp)  # 用list()复制一个新的列表，否则pop之后，res内的结果也没有了
                res.append(tmp1)
            return
        for i in range(index, len(nums)):
            tmp.append(nums[i])
            helper(res, tmp, nums, target - nums[i], i)
            tmp.pop()

    helper(res, [], nums, target, 0)
    return res


def trapRainWater(height: List[int]) -> int:
    """42.接雨水"""
    """单调递减栈"""
    n = len(height)
    stack = []
    res = 0
    curIndex = 0
    while curIndex < n:
        # 当栈不为空且curIndex的值大于顶元素时，即违背单调递减的情况
        while (len(stack) > 0 and height[curIndex] > height[stack[-1]]):
            top = stack.pop()
            if len(stack) <= 0:
                break
            # 如果栈内有元素，求面积
            h = min(height[stack[-1]], height[curIndex]) - height[top]
            dist = curIndex - stack[-1] - 1
            res += dist * h
        stack.append(curIndex)
        curIndex += 1
    return res


if __name__ == '__main__':
    # print("binarySearch", binarySearch([5, 7, 7, 8, 8, 10], 8))
    # print("combinationSum", combinationSum([2, 3, 6, 7], 7))
    print("trapRainWater", trapRainWater([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))
