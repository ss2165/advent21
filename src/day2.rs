use crate::read::read_lines;

pub fn follow_instructions(path: &str) -> (i32, i32) {
    let insts = read_lines(path).unwrap().map(|line| {
        let line = line.unwrap();
        let mut split = line.split_whitespace();
        match (split.next().unwrap(), split.next().unwrap()) {
            ("forward", num) => (num.parse().unwrap(), 0),
            ("down", num) => (0, num.parse().unwrap()),
            ("up", num) => (0, -(num.parse::<i32>().unwrap())),
            _ => panic!(),
        }
    });
    let (hor, dep): (Vec<_>, Vec<_>) = insts.unzip();

    (hor.iter().sum(), dep.iter().sum())
}

pub fn follow_instructions_aim(path: &str) -> (i32, i32) {
    let (mut hor, mut dep, mut aim) = (0, 0, 0);

    for line in read_lines(path).unwrap() {
        let line = line.unwrap();
        let mut split = line.split_whitespace();
        match (split.next().unwrap(), split.next().unwrap()) {
            ("forward", num) => {
                let num: i32 = num.parse().unwrap();
                hor += num;
                dep += aim * num;
            }
            ("down", num) => aim += num.parse::<i32>().unwrap(),
            ("up", num) => aim -= num.parse::<i32>().unwrap(),
            _ => panic!(),
        };
    }
    // let (hor, dep): (Vec<_>, Vec<_>)  = insts.unzip();

    // (hor.iter().sum(), dep.iter().sum())
    (hor, dep)
}
