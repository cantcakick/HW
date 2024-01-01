fun main() {
    for (i in 1..10) {
        val numberOfSpaces = i-1
        for (j in 1 ..numberOfSpaces) {
            print(" ")
        }
        val numberOfStars = 11 - i
        for (j in 1.. numberOfStars){
            print("*")}
        println()
    }
}