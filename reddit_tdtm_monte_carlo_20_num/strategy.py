class Strategy:
    def __init__(self) -> None:
        self.nums = [ None for _ in range(20) ]

    # Find optimal placement for number
    # Returns true if successfully placed
    def place(self, new_num: int) -> bool:
        # Determine which "range" this number fits in.
        low = -1
        high = 20
        for i, num in enumerate(self.nums):
            if num is not None:
                if num < new_num:
                    low = i
                elif num > new_num:
                    high = i
                    break
                else:
                    # Numbers are equal
                    return False
        
        # We have found a min and max values, now determine most "optimal" slot
        if low >= high - 1:
            return False
        
        lowval = self.nums[low] if low >= 0 else 0
        highval = self.nums[high] if high < 20 else 1000
        optimal = round((high - low - 2) * ((new_num - lowval) / (highval - lowval))) + low + 1

        self.nums[optimal] = new_num

        return True
    
    def __str__(self) -> str:
        return ','.join(str(n) for n in self.nums)
    def __repr__(self) -> str:
        return self.__str__()