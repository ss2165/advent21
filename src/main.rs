mod day1;
mod day2;
mod day3;
mod read;

fn day1_main() {
    println!("{}", day1::part_b("./inputs/day1_a.txt"));
}

fn day2_main() {
    let (hor, dep) = day2::follow_instructions_aim("./inputs/day2.txt");
    println!("{:?}", (hor * dep));
}

fn day3_main() {
    let (gam, eps) = day3::gamma_epsilon("./inputs/day3.txt");
    println!("{:?}", gam * eps);
}

fn day3_part2_main() {
    let ox = day3::to_u32(&day3::filter_tree("./inputs/day3.txt", |zer, one| {
        zer > one
    }));
    let c2 = day3::to_u32(&day3::filter_tree("./inputs/day3.txt", |zer, one| {
        zer <= one
    }));

    println!("{:?}", ox * c2);

}

fn main() {
    day3_part2_main();
}
