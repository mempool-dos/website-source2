from django.shortcuts import render

# Create your views here.
import matplotlib.pyplot as plt
import io
import urllib, base64

import requests
from time import sleep
from bs4 import BeautifulSoup

from mdutils.mdutils import MdUtils


def crawler():
    count = 0
    all_writer_list = []
    writer_list = []
    for i in range(0,1000):
        print(i)
        sleep(0.5)
        url = 'https://etherscan.io/blocks?ps=100&p='+str(i)
        headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0'}
        response = requests.get(url, headers=headers)
        content = response.content
        # print(content)
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup)
        for row in soup.select('table.table-hover tbody tr'):
            # print(row)
            cells1 = row.findAll('td')
            cells = map(lambda x: x.text, cells1)
            if len(cells1) == 10:
                block, Time, age, txn, Fee_Recipient, gas_used, gas_limit, base_fee, reward, burnt_fees= cells
                # print(block+'~~~'+Time+'~~~'+age+'~~~'+txn+'~~~'+'~~~'+Fee_Recipient+'~~~'+gas_used+'~~~'+gas_limit+'~~~'+base_fee+'~~~'+reward)
                # print(gas_used)
                Fee_Recipient = "0xDAFEA492D9c6733ae3d56b7Ed1ADB60692c98Bc5"
                templist = [block, Time, age, txn, Fee_Recipient, gas_used, gas_limit, base_fee, reward, burnt_fees]
                all_writer_list.append(templist)
                # print(templist[5])
                if float(gas_used.split('(')[1].split('%')[0])<0.1:
                    count+=1
                    print(templist)
                    writer_list.append(templist)
    return all_writer_list,writer_list

def scraper(_miner,all_writer_list,writer_list):
    catch_block_number = []
    block_number = []
    for row in all_writer_list:
        if row[4] == _miner:
            block_number.append(row[0])
    for row in writer_list:
        if row[4] == _miner:
            catch_block_number.append(row[0])
    return catch_block_number, block_number

def Find_sequence(catch_data_series,data_series):
    if data_series[0] != catch_data_series[0]:
        return 0
    else:
        if len(catch_data_series)<2 or len(data_series)<2:
            return 1
        else:
            return 1 + Find_sequence(catch_data_series[1:],data_series[1:])

def plot_png(all_writer_list, writer_list):
    all_data = []
    miner = []
    line_count = 0

    # for row in writer_list:
    #     dic_block = {}
    #     dic_block['block'] = row[0]
    #     dic_block['miner'] = row[4]
    #     if row[4] not in miner:
    #         miner.append(row[4])
    #     all_data.append(dic_block)
    height = [0, 0, 0, 0, 0]

    # for each_miner in miner:
    #     catch_block_number_list, block_number_list = scraper(each_miner,all_writer_list,writer_list)
    #     for i in range(len(catch_block_number_list)):
    #         for j in range(len(block_number_list)):
    #             if block_number_list[j] == catch_block_number_list[i]:
    #                 sequence_length = Find_sequence(catch_block_number_list[i:], block_number_list[j:])
    #                 i += sequence_length - 1
    #                 j += sequence_length - 1
    #                 height[sequence_length - 1] += 1
    print(writer_list)
    consecutive_1 = []
    consecutive_2 = []

    sequence = []
    for i in range(len(writer_list)):
        print(i)
        print(writer_list[i])
        sequence_len = 1
        sequence.append(writer_list[i])
        for j in range(i + 1, len(writer_list)):
            print(int(writer_list[i][0]) - j + i)
            if int(writer_list[i][0]) - j + i == int(writer_list[j][0]):
                sequence_len += 1
                sequence.append(writer_list[j])
            else:
                height[sequence_len - 1] += 1
                if sequence_len ==1:
                    consecutive_1.extend(sequence)
                if sequence_len ==2:
                    consecutive_2.append(sequence)
                i = j
                sequence = []
                break

            # if writer_list[i]

    # x-coordinates of left sides of bars
    left = [1, 2, 3, 4, 5]
    # labels for bars
    tick_label = ['1', '2', '3', '4', '5']

    # plotting a bar chart
    plt.bar(left, height, tick_label=tick_label,
            width=0.8, color=['blue'])

    # naming the x-axis
    plt.xlabel('sequence_length')
    # naming the y-axis
    plt.ylabel('Number of instances')
    # plot title
    plt.title('Empty blocks!')
    # plt.show()
    plt.savefig('Deter_plot.png')
    return consecutive_1, consecutive_2


def make_down(consecutive_1, consecutive_2, writer_list):
    mdFile = MdUtils(file_name='index')
    mdFile.write(
        "#<span class=\"label\" style=\"background-color: white; color: rgb(0, 153, 51);border: 1px solid rgb(0, 153, 51);border-radius: 5px;\">MempoolDoS</span>: Detecting attacks of Ethereum mempool DoS")

    mdFile.new_header(level=2, title="Found empty blocks")
    mdFile.write("\n\n")
    mdFile.write("In the last 100000 blocks, we found "+str(len(writer_list))+" empty blocks whose Gas utilization is less than 0.1%.")
    mdFile.write("\n")
    mdFile.write("![Screenshot](img/Deter_plot.png)")
    mdFile.write("\n\n")
    mdFile.write("Recent empty blocks: ")
    mdFile.write("\n")
    list_of_strings = ["Height", "Gas utilization", "Web link"]
    for line in consecutive_1:
        list_of_strings.extend([line[0], line[5],mdFile.new_reference_link(link='https://etherscan.io/block/'+str(line[0]),text='Block '+str(line[0]))])
    mdFile.new_line()
    mdFile.new_table(columns=3, rows=len(consecutive_1)+1, text=list_of_strings, text_align='center')
    mdFile.write("\n\n")
    mdFile.write("Recent consecutive empty blocks:  ")
    mdFile.write("\n")
    if len(consecutive_2)==0:
        mdFile.write("Sorry, There is no consecutive empty blocks in recent 100000 blocks.")
    else:
        list_of_strings = ["Height", "Gas utilization", "Web link"]
        for line in consecutive_2:
            list_of_strings.extend([line[0][0], line[0][5], mdFile.new_reference_link(link='https://etherscan.io/block/'+str(line[0][0]),text='Block '+str(line[0][0]))])
            list_of_strings.extend([line[1][0], line[1][5], mdFile.new_reference_link(link='https://etherscan.io/block/'+str(line[1][0]),text='Block '+str(line[1][0]))])
            list_of_strings.extend(["   ","   ","   "])
        mdFile.new_table(columns=3, rows=len(consecutive_2)*3 + 1, text=list_of_strings, text_align='center')
    mdFile.create_md_file()



if __name__ == '__main__':
    all_writer_list, writer_list = crawler()
    consecutive_1, consecutive_2 = plot_png(all_writer_list, writer_list)
    make_down(consecutive_1, consecutive_2,writer_list)



