def classify(data):
    total, prior_1, prior_2, leave = [data[0][:]], [data[0][:]], [data[0][:]], [data[0][:]]
    total[0].extend(['Nhóm khách hàng'])
    for row in range(1, len(data)):
        cols = data[row][:]
        if int(cols[10]) and int(cols[11]) > 1:
            tmp = data[row][:]
            tmp[0] = len(leave)
            leave.append(tmp)
            cols.append('Dự đoán rời mạng')
        else:
            means_postage = (cols[6] + cols[7] + cols[8] + cols[9]) / 4
            postage_rate = means_postage / cols[6]
            if postage_rate >= 1.1:
                tmp = data[row][:]
                tmp[0] = len(prior_1)
                prior_1.append(tmp)
                cols.append('Nhóm Ưu tiên 1')
            elif postage_rate > 0.7:
                tmp = data[row][:]
                tmp[0] = len(prior_2)
                prior_2.append(tmp)
                cols.append('Nhóm Ưu tiên 2')
            else:
                tmp = data[row][:]
                tmp[0] = len(leave)
                leave.append(tmp)
                cols.append('Dự đoán rời mạng')
        total.append(cols)

    return total, prior_1, prior_2, leave
