import matplotlib.pyplot as plt
import json
import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
from table_generate import commit_count_per_repo


def load_data(data_path):
    with open(data_path) as f:
        data = json.load(f)
    repos = []
    frequencies = [[] for _ in range(4)]
    for repo in data.keys():
        repos.append(repo)
        frequencies[0].append(data[repo]["2by2"])
        frequencies[1].append(data[repo]["3by3"])
        frequencies[2].append(data[repo]["4by4"])
        frequencies[3].append(data[repo]["5by5"])

    return repos, frequencies


def box_plot(repos, frequencies):
    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create subplots for each boxplot
    fig, axes = plt.subplots()

    # load data as DF
    df = pd.DataFrame({
        '2': frequencies[0],
        '3': frequencies[1],
        '4': frequencies[2],
        '5': frequencies[3],
    })

    # draw
    sns.boxplot(data=df)

    # Adjust layout to prevent overlap
    # plt.tight_layout()

    # set labels and titles
    axes.set(ylim=(-0.02, 0.7))
    axes.set_xlabel("granularity level")
    axes.set_ylabel("frequency")
    # The CGRs exclude the CGRs generated in the lower-granularity CGRs are called as (filtered)
    # axes.set_title("Frequency of CGRs (filtered) at each granularity level")
    # axes.set_title("Frequency of FGRs at each granularity level")
    axes.set_title("Frequency of CGRs at each granularity level")
    # plt.savefig("figures/frequency_FGR.pdf", format="pdf")
    # plt.savefig("figures/frequency_filtered.pdf", format="pdf")
    plt.savefig("figures/frequency_cgr_normal.pdf", format="pdf")

    plt.show()

    return frequencies


def box_plot_two_groups(frequencies_filter, frequencies_no_filter):
    """
    two groups of boxes, each contains 4 boxes, each box represents one granularity level
    the 1st group is the CGR frequencies excluding CGRs detected from lower graunlarity
    the 2nd group is not excluding
    :return:
    """
    sns.set(style="whitegrid")

    frequencies_filter_sequence = []
    for each in frequencies_filter:
        frequencies_filter_sequence += each
    frequencies_no_filter_sequence = []
    for each in frequencies_no_filter:
        frequencies_no_filter_sequence += each

    d = {
        'frequency': frequencies_filter_sequence + frequencies_no_filter_sequence,
        'granularity_level': [str(j) for j in range(2, 6) for i in range(len(frequencies_filter[0]))] + [str(j) for j in
                                                                                                         range(2, 6) for
                                                                                                         i in range(
                len(frequencies_no_filter[0]))],
        'CGR type': ['CGR' for _ in range(len(frequencies_filter_sequence))] + ['CGR ' for _ in range(
            len(frequencies_no_filter_sequence))]
    }

    df = pd.DataFrame(d)

    fig = sns.boxplot(x='granularity_level', y='frequency', data=df, hue='CGR type', order=['2', '3', '4', '5'],
                      palette='Set2')

    # Add labels and title
    plt.xlabel('Granularity Level')
    plt.ylabel('CGR Frequency')
    plt.title('Boxplot of CGR frequencies')

    # Adjust layout to prevent overlap
    plt.tight_layout()
    # plt.savefig("figures/frequency_CGR_two.pdf", format="pdf")
    plt.show()


def positive_correlation_ratio(frequencies):
    def is_positive_correlation(data):
        for i in range(len(data) - 1):
            if data[i] > data[i + 1]:
                return False
        return True

    positive_correlation_count = 0
    for i in range(len(frequencies[0])):
        if is_positive_correlation([frequencies[j][i] for j in range(len(frequencies))]):
            positive_correlation_count += 1

    return positive_correlation_count / len(frequencies[0])


def get_man_whiteney_u_test(data1, data2):
    temp1, temp2 = [], []
    for each in data1:
        temp1 += each
    for each in data2:
        temp2 += each
    print(len(temp1))
    print(len(temp2))
    statistic, p_value = stats.mannwhitneyu(temp1, temp2)
    print(p_value)


def get_statistical_values(data):
    maximum_values = []
    median_value = []
    minimum_values = []
    for i, dataset in enumerate(data):
        maximum_values.append(np.max(dataset))
        median_value.append(np.median(dataset))
        minimum_values.append(np.min(dataset))
    return maximum_values, median_value, minimum_values


def spearman_correlation_coefficient(labels, data):
    def interpretation(rho, p_value):
        if p_value < 0.05:
            if rho == 1:
                print("There is a perfect positive monotonic relationship.")
            elif rho == -1:
                print("There is a perfect negative monotonic relationship.")
            elif rho > 0:
                print(rho)
                print("There is a positive monotonic relationship.")
            elif rho < 0:
                print("There is a negative monotonic relationship.")
        else:
            print("There is no significant monotonic relationship.")

    rho, p = stats.spearmanr(data[0], data[1])
    interpretation(rho, p)
    rho, p = stats.spearmanr(data[1], data[2])
    interpretation(rho, p)
    rho, p = stats.spearmanr(data[2], data[3])
    interpretation(rho, p)


def frequency_increase_ratio_of_each_repository(labels, data):
    res = {}
    print(data)
    for j in range(1, len(data)):
        for i in range(len(data[j])):
            if labels[i] not in res.keys():
                res[labels[i]] = {}
            print(data[j][i], data[j - 1][i])
            res[labels[i]][j] = data[j][i] / data[j - 1][i]
    print(res)


def one_way_anova(labels, data):
    s, p = stats.f_oneway(data[0], data[1], data[2], data[3])
    print(p)


def search_highest_frequency(labels, data):
    for i in range(len(data)):
        maximum_value = max(data[i])
        repo = labels[data[i].index(maximum_value)]
        print(f"The maximum value at granularity level {i + 2} is in {repo}, the value is {maximum_value}")


def data_analysis_of_box_plot(labels, data):
    for i, dataset in enumerate(data):
        maximum_values = np.max(dataset)
        median_value = np.median(dataset)
        minimum_values = np.min(dataset)
        print(f"for granularity {labels[i]}")
        print(f"minimum value: {minimum_values}")
        print(f"median value: {median_value}")
        print(f"maximum value: {maximum_values}")


def print_average_values(data):
    for each in data:
        print(sum(each) / len(each))


def boxplot_normal_frequency():
    """
    draw the # of CGR pergranularity/ # of normal commits for each repository
    :return:
    """
    with open("./RQ1_normal_frequency.json") as f:
        data = json.load(f)
    count = []
    for granularity in range(2, 6):
        count.append([])
        for repo in data:
            count[granularity - 2].append(data[repo][str(granularity)])
    # total
    count.append([])
    for repo in data:
        cur = sum([data[repo][each] for each in data[repo]])
        count[4].append(cur)

    sns.set(style="whitegrid")

    fig, axes = plt.subplots()
    df = pd.DataFrame({
        '2': count[0],
        '3': count[1],
        '4': count[2],
        '5': count[3],
        '2+3+4+5': count[4]
    })
    sns.boxplot(data=df)
    axes.set(ylim=(-0.02, 0.7))
    axes.set_xlabel("granularity level")
    axes.set_ylabel("frequency")
    axes.set_title("Frequency of CGRs at each granularity level")
    # plt.savefig("figures/frequency_cgr_normal.pdf", format="pdf")
    plt.show()


def boxplot_frequency_per_effective_squash_unit(frequencies, save=False):
    """

    :param frequencies:
    :return:
    """
    sns.set(style="whitegrid")
    d = {}
    for i in range(2, 6):
        d[str(i)] = frequencies[i - 2]
    df = pd.DataFrame(d)
    fig = sns.boxplot(data=df)
    plt.xlabel('Granularity Level')
    # plt.ylabel('CGR Frequency')
    # plt.title('Boxplot of CGR frequencies')
    plt.ylabel('CGR  Frequency')  # for CGR-
    plt.title('Boxplot of CGR  frequencies') # for CGR-
    plt.tight_layout()
    if save:
        # plt.savefig("figures/frequency_CGR.pdf", format="pdf")
        plt.savefig("figures/frequency_CGR-.pdf", format="pdf")
    plt.show()


if __name__ == "__main__":
    filtered_data = "RQ1_frequency_filter.json"
    without_filter_data = "RQ1_frequency_no_filter.json"
    FGR_frequency_data = "RQ2_FGR_frequency.json"

    repos, frequencies = load_data(filtered_data)
    # print(len(repos))

    repos, frequencies_no_filter = load_data(without_filter_data)
    # box_plot_two_groups(frequencies, frequencies_no_filter)
    # data_analysis_of_box_plot(range(2, 6), frequencies)
    # data_analysis_of_box_plot(range(2,6), frequencies_no_filter)
    # print("positive correlation ratio is:", poszitive_correlation_ratio(frequencies))
    # one_way_anova(range(2, 6), frequencies)
    # spearman_correlation_coefficient(range(2, 6), frequencies)

    # frequency_increase_ratio_of_each_repository(repos, frequencies)

    # repos_no_filter, frequencies_no_filter = load_data(without_filter_data)
    get_man_whiteney_u_test(frequencies, frequencies_no_filter)
    # box_plot(repos, frequencies_no_filter)

    # search_highest_frequency(repos, frequencies)

    # print_average_values(frequencies)

    # repos, FGR_frequencies = load_data(FGR_frequency_data)
    # data_analysis_of_box_plot(range(2, 6), FGR_frequencies)
    # print_average_values(FGR_frequencies)
    # box_plot(repos, FGR_frequencies)

    # calculate the # of CGR pergranularity/ # of normal commits
    # boxplot_normal_frequency()

    # redraw frequency per effective squash unit
    # boxplot_frequency_per_effective_squash_unit(frequencies, save=True)
    boxplot_frequency_per_effective_squash_unit(frequencies_no_filter, save=True)
