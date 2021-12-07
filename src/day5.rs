use std::{collections::HashMap, hash::Hash};

use crate::read::read_lines;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
struct Point(u32, u32);

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
        if (line.start.0 != line.end.0) & (line.start.1 != line.end.1) {
            return;
        }

        for x in line.start.0..line.end.0 + 1 {
            for y in line.start.1..line.end.1 + 1 {
                *self.map.entry(Point(x, y)).or_insert(0) += 1;
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
        let nums: Vec<u32> = commas.split(",").map(|x| x.parse().unwrap()).collect();
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

    println!("{:?}", lm.map);
}
