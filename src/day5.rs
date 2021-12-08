use std::{collections::HashMap, hash::Hash};

use crate::read::read_lines;

#[derive(Debug, Clone, Hash, PartialEq, Eq, PartialOrd, Ord)]
struct Point(i32, i32);

#[derive(Debug, Clone)]
struct Line {
    pub start: Point,
    pub end: Point,
}
#[derive(Debug)]
struct LineMap {
    map: HashMap<Point, u32>,
}

impl Default for LineMap {
    fn default() -> Self {
        Self {
            map: Default::default(),
        }
    }
}
impl LineMap {
    fn new(map: HashMap<Point, u32>) -> Self {
        Self { map }
    }

    fn add_line(&mut self, line: Line) {
        let mut endpoints = [line.start, line.end];
        endpoints.sort();
        let [start, end] = endpoints;
        // dbg!(&start, &end);
        if (start.0 == end.0) | (start.1 == end.1) {
            for x in start.0..end.0 + 1 {
                for y in start.1..end.1 + 1 {
                    *self.map.entry(Point(x, y)).or_insert(0) += 1;
                }
            }
        } else if (end.0 - start.0).abs() == (end.1 - start.1).abs() {
            let n_steps = (end.1 - start.1).abs();
            let xsign = (end.0 - start.0)/n_steps;
            let ysign = (end.1 - start.1)/n_steps;



            for step in  0..(n_steps+1) {
                *self
                    .map
                    .entry(Point(start.0 + step*xsign, start.1 + step*ysign))
                    .or_insert(0) += 1;
            }
        }
    }

    fn n_overlap_points(&self, n: u32) -> usize {
        self.map
            .iter()
            .filter(|(_, overlaps)| overlaps >= &&n)
            .count()
    }
}

fn parse_input(path: &str) -> Vec<Line> {
    let mut out = vec![];
    fn commas_to_point(commas: &str) -> Point {
        let nums: Vec<i32> = commas.split(",").map(|x| x.parse().unwrap()).collect();
        Point(nums[0], nums[1])
    }
    for line in read_lines(path).unwrap() {
        let line = line.unwrap();
        let points = line.split(" -> ").collect::<Vec<_>>();

        let start = points[0];
        let end = points[1];
        out.push(Line {
            start: commas_to_point(start),
            end: commas_to_point(end),
        });
    }

    out
}
pub fn test_map(path: &str) {
    let mut lm = LineMap::default();

    let lines = parse_input(path);
    for line in lines {
        lm.add_line(line);
    }

    // print_grid(&lm);
    println!("{:?}", lm.n_overlap_points(2));
}

fn print_grid(lm: &LineMap) {
    let mut s = "".to_string();
    for i in 0..10 {
        for j in 0..10 {
            s += &lm
                .map
                .get(&Point(j, i))
                .map(|i| format!("{}", i))
                .unwrap_or(".".to_string());
        }
        s += "\n";
    }
    println!("{}", s);
}
