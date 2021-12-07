use crate::read::read_lines;

fn bitstr_iter(path: &str) -> impl Iterator<Item = Vec<bool>> + '_ {
    let lines = read_lines(path).unwrap();
    lines.map(|line| {
        line.unwrap()
            .chars()
            .into_iter()
            .map(|c| c.to_digit(10).unwrap() != 0)
            .collect()
    })
}

fn count_bits(path: &str) -> Vec<bool> {
    let lines = read_lines(path).unwrap();
    let width = lines.map(Result::unwrap).next().unwrap().len();

    let init: Vec<u32> = vec![0; width];
    let mut count: u32 = 0;
    let res = bitstr_iter(path).fold(init, |accum, elem| {
        count += 1;
        elem.iter().zip(accum).map(|(x, y)| *x as u32 + y).collect()
    });
    println!("count {}", count);
    // let comp = if pref_one {}
    res.iter().map(|sum| (sum > &(count / 2))).collect()
}

pub fn to_u32<T>(slice: &[T]) -> u32
where
    T: Into<u32> + Copy,
{
    let mut slice = slice.to_owned();
    slice.reverse();
    slice
        .iter()
        .fold((0, 1), |(acc, mul), &bit| {
            (acc + (mul * (1 & bit.into())), mul.wrapping_add(mul))
        })
        .0
}

fn find_other(val: u32, bitwidth: usize) -> u32 {
    (1 << bitwidth as u32) - 1 - val
}

pub fn gamma_epsilon(path: &str) -> (u32, u32) {
    let gamma_bits = count_bits(path);

    let gamma = to_u32(&gamma_bits);

    (gamma, find_other(gamma, gamma_bits.len()))
}

#[derive(Debug)]
struct Node(Option<Box<Node>>, Option<Box<Node>>);

impl Default for Node {
    fn default() -> Self {
        Self(None, None)
    }
}

impl Node {
    fn count_entries(&self, acc: u32) -> u32 {
        match self {
            Node { 0: None, 1: None } => acc + 1,
            Node {
                0: Some(zer),
                1: None,
            } => zer.count_entries(acc),
            Node {
                0: None,
                1: Some(one),
            } => one.count_entries(acc),
            Node {
                0: Some(zer),
                1: Some(one),
            } => {
                let acc = one.count_entries(acc);
                zer.count_entries(acc)
            }
        }
    }

    pub fn bitstrings(&self, acc: &mut Vec<Vec<bool>>, curr: &mut Vec<bool>) {
        match self {
            Node { 0: None, 1: None } => acc.push(curr.clone()),
            Node {
                0: Some(zer),
                1: None,
            } => {
                curr.push(false);
                zer.bitstrings(acc, curr);
            }
            Node {
                0: None,
                1: Some(one),
            } => {
                curr.push(true);
                one.bitstrings(acc, curr);
            }
            Node {
                0: Some(zer),
                1: Some(one),
            } => {
                let mut zerocurr = curr.clone();
                zerocurr.push(false);
                zer.bitstrings(acc, &mut zerocurr);

                curr.push(true);
                one.bitstrings(acc, curr);
            }
        }
    }
}

#[derive(Debug)]
struct BinTree(Node);

impl BinTree {
    pub fn new() -> Self {
        Self(Node::default())
    }

    pub fn insert_bits<I>(node: &mut Node, mut iter: I)
    where
        I: Iterator<Item = bool>,
    {
        match iter.next() {
            Some(true) => {
                let nextnode = node.1.get_or_insert(Box::new(Node::default()));
                Self::insert_bits(nextnode, iter);
            }
            Some(false) => {
                let nextnode = node.0.get_or_insert(Box::new(Node::default()));
                Self::insert_bits(nextnode, iter);
            }
            None => (),
        };
    }

    pub fn from_bits<I, G>(iter: I) -> Self
    where
        I: IntoIterator<Item = G>,
        G: IntoIterator<Item = bool>,
    {
        let mut new = Self::new();
        for bititer in iter {
            Self::insert_bits(&mut new.0, bititer.into_iter());
        }
        new
    }

    pub fn all_bitstr(&self) -> Vec<Vec<bool>> {
        let mut acc = vec![];
        let mut curr = vec![];

        self.0.bitstrings(&mut acc, &mut curr);
        acc
    }
}

pub fn filter_tree(path: &str, comp: fn(u32, u32) -> bool) -> Vec<u8> {
    let mut tree = BinTree::from_bits(bitstr_iter(path));

    let mut curr_node = &mut tree.0;

    loop {
        let zer_count = curr_node.0.as_ref().map_or(0, |n| n.count_entries(0));
        let one_count = curr_node.1.as_ref().map_or(0, |n| n.count_entries(0));
        match (zer_count, one_count) {
            (1, 0) | (0, 1) | (0, 0) => break,
            _ => (),
        };
        if comp(zer_count, one_count) {
            curr_node.1.take();
            curr_node = curr_node.0.as_deref_mut().unwrap();
        } else {
            curr_node.0.take();
            curr_node = curr_node
                .1
                .as_deref_mut()
                .expect(&format!("{}, {}", zer_count, one_count));
        }
    }
    dbg!(tree.0.count_entries(0));
    tree.all_bitstr()
        .remove(0)
        .into_iter()
        .map(Into::into)
        .collect()
}

pub fn test_tree(path: &str) {
    let tree = BinTree::from_bits(bitstr_iter(path));

    let bitstr: Vec<Vec<u8>> = tree
        .all_bitstr()
        .iter()
        .map(|bs| bs.iter().map(|x| *x as u8).collect())
        .collect();

    println!("{:?}", bitstr);
}

/*
part 2 plan

 */
