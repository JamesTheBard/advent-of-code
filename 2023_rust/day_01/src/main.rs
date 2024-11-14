use regex::Regex;
use std::fs;
use std::sync::LazyLock;

static RE_BEGIN: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r"(\d|one|two|three|four|five|six|seven|eight|nine)").unwrap());
static RE_END: LazyLock<Regex> =
    LazyLock::new(|| Regex::new(r".*(\d|one|two|three|four|five|six|seven|eight|nine)").unwrap());

fn main() {
    let contents = fs::read_to_string("data.txt").unwrap();
    let mut day_01 = 0;
    let mut day_02 = 0;

    for line in contents.split("\n") {
        day_01 += get_calibration_data(line, false);
        day_02 += get_calibration_data(line, true);
    }

    println!("Part 1: {}", day_01);
    println!("Part 2: {}", day_02);
}

fn get_calibration_data(line: &str, include_strings: bool) -> i32 {
    let mut total = 0;

    if include_strings {
        let re_start_match = RE_BEGIN.captures(line);
        let re_end_match = RE_END.captures(line);

        match re_start_match {
            Some(result) => {
                let r = result.get(1).unwrap();
                match r.as_str() {
                    "one"   => total += 1,
                    "two"   => total += 2,
                    "three" => total += 3,
                    "four"  => total += 4,
                    "five"  => total += 5,
                    "six"   => total += 6,
                    "seven" => total += 7,
                    "eight" => total += 8,
                    "nine"  => total += 9,
                    _       => total += r.as_str().parse::<i32>().unwrap(),
                }
                total *= 10;
            }
            None => return total,
        }

        match re_end_match {
            Some(result) => {
                let r = result.get(1).unwrap();
                match r.as_str() {
                    "one"   => total += 1,
                    "two"   => total += 2,
                    "three" => total += 3,
                    "four"  => total += 4,
                    "five"  => total += 5,
                    "six"   => total += 6,
                    "seven" => total += 7,
                    "eight" => total += 8,
                    "nine"  => total += 9,
                    _       => total += r.as_str().parse::<i32>().unwrap(),
                }
            }
            None => (),
        }
    } else {
        let v: Vec<&str> = line.matches(char::is_numeric).collect();
        if v.is_empty() {
            return total;
        };

        total = String::from(format!("{}{}", v[0], v[v.len() - 1]))
            .parse::<i32>()
            .unwrap();
    }

    return total;
}
