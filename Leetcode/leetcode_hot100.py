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


if __name__ == '__main__':
    # print("binarySearch", binarySearch([5, 7, 7, 8, 8, 10], 8))
    print("combinationSum", combinationSum([2, 3, 6, 7], 7))
