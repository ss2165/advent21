use crate::read::read_lines;

const N: usize = 5;
#[derive(Debug)]
struct Board {
    vals: [[(u32, bool); N]; N],
    row_check: [bool; N],
    col_check: [bool; N],
}

impl Board {
    fn new<I, G>(board_elems: I) -> Self
    where
        I: IntoIterator<Item = G>,
        G: IntoIterator<Item = u32>,
    {
        let mut vals = [[(0, false); N]; N];
        for (i, row) in board_elems.into_iter().enumerate() {
            for (j, elem) in row.into_iter().enumerate() {
                vals[i][j].0 = elem;
            }
        }
        Self {
            vals,
            row_check: [false; N],
            col_check: [false; N],
        }
    }

    fn mark_num(&mut self, num: u32) -> bool {
        let found = self.vals.iter().enumerate().find_map(|(i, row)| {
            row.iter().enumerate().find_map(
                |(j, elem)| {
                    if elem.0 == num {
                        Some((i, j))
                    } else {
                        None
                    }
                },
            )
        });

        if let Some((i, j)) = found {
            self.vals[i][j].1 = true;
            self.row_check[i] = self.vals[i].iter().all(|(_, mark)| *mark);
            self.col_check[j] = self.vals.iter().all(|row| row[j].1);
            return self.row_check[i] | self.col_check[j];
        }
        false
    }

    fn score(&self) -> u32 {
        self.vals
            .iter()
            .map(|row| {
                row.iter()
                    .filter_map(|(num, mark)| (!mark).then(|| *num))
                    .sum::<u32>()
            })
            .sum()
    }
}

fn parse_input(path: &str) -> (Vec<u32>, Vec<Board>) {
    let mut lines = read_lines(path).unwrap();

    let nums: Vec<u32> = lines
        .next()
        .unwrap()
        .unwrap()
        .split(",")
        .map(|x| x.parse().unwrap())
        .collect();

    let lines: Vec<_> = lines.collect();
    let mut boards = vec![];
    for chunk in lines.chunks(N + 1) {
        let board_lines: Vec<Vec<u32>> = chunk[1..]
            .iter()
            .map(|line| {
                line.as_ref()
                    .unwrap()
                    .split_whitespace()
                    .map(|num| num.parse().unwrap())
                    .collect()
            })
            .collect();

        boards.push(Board::new(board_lines));
    }

    (nums, boards)
}

fn first_winning_board(nums: Vec<u32>, mut boards: Vec<Board>) -> Option<(u32, u32)> {
    for num in nums {
        for board in boards.iter_mut() {
            if board.mark_num(num) {
                return Some((num, board.score()));
            }
        }
    }
    None
}

fn last_winning_board(nums: Vec<u32>, mut boards: Vec<Board>) -> Option<(u32, u32)> {
    for num in nums {
        let n_boards = boards.len();
        let mut completed_boards = vec![];
        for (board_index, board) in boards.iter_mut().enumerate() {
            if board.mark_num(num) {
                if n_boards == 1 {
                    return Some((num, board.score()));
                } else {
                    completed_boards.push(board_index);
                }
            }
        }
        completed_boards.sort();
        completed_boards.reverse();
        for board_i in completed_boards {
            boards.remove(board_i);
        }
    }

    None
}
pub fn test_parse(path: &str) {
    let (nums, mut boards) = parse_input(path);

    println!("{:#?}", last_winning_board(nums, boards));
}
