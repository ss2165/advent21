use crate::read::read_lines;

fn get_nums(path: &str) -> Vec<u32> {
    let lines = read_lines(path).unwrap();
    lines
        .map(|line| line.unwrap().parse::<u32>().unwrap())
        .collect()
}
fn count_increase(nums: Vec<u32>) -> u32 {
    nums.windows(2).map(|pair| (pair[1] > pair[0]) as u32).sum()
}

pub fn part_a(path: &str) -> u32 {
    count_increase(get_nums(path))
}

pub fn part_b(path: &str) -> u32 {
    let nums = get_nums(path);
    let win3_sums: Vec<u32> = nums.windows(3).map(|win| win.iter().sum()).collect();
    count_increase(win3_sums)
}
