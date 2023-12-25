

import triangleArea//Basic
import getPoints
/*
fun main() {
    val height = 5
    for (i in 1..height) {
        for (j in 1..i) {
            print("*")
        }
        println()
    }
}
*/
//Using functions
/* 
fun printStars(num: Int) {
    for (j in 1..num) {
        print("*")
    }
    println()
}
fun main() {
    val height = 5
    for (i in 1..height) {
        printStars(i)
    }
}
*/
//Functions with Return
fun triangleArea(width: double, height: double): double{
    return width * height / 2
}
fun main(){
    val area: Double = triangleArea(1.0, 2.0)
    println(area)
    println(triangleArea(5.0, 22.0))
}

fun getPoints(basePoints: Int, boost:Int): Int{
    return basePoints * boost
}
fun main() {
    var score = 0;
println(score)
    score += getPoints(10, 1)
println(score)
    score += getPoints(20, 2)
println(score)
    score += getPoints(150, 12)
}