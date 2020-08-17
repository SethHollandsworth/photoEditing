import numpy as np
import concurrent.futures


def test(row):
    # print(row)
    row[0] = 0
    return row


if __name__ == "__main__":
    rows = [0, 1]
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([1, 2, 3])
    # with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
    #     for b in executor.map(test, a):
    #         print(b)
    # test(a[0])
    # print(a)
    print(np.argmax(b <= 2))
