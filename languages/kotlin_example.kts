import kotlin.math.*

infix fun Int.greaterThanExp(x: Int) = this > exp(x.toFloat())

fun factorial(x: Int): Int = when (x) {
    0    -> 1
    else -> x * factorial(x - 1)
}

println(factorial(5) greaterThanExp 6)
println(factorial(6) greaterThanExp 7)
println(factorial(7) greaterThanExp 8)
