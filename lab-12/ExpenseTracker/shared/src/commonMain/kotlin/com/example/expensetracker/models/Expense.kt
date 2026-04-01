package com.example.expensetracker.models
import kotlinx.datetime.*
import kotlinx.serialization.Serializable
@Serializable
data class Category(val id: Long, val name: String, val color: String, val icon: String, val isDefault: Boolean = false)
@Serializable
data class Expense(val id: Long, val amount: Double, val categoryId: Long, val description: String?, val date: Instant, val isSynced: Boolean = false) {
    fun isValid(): Boolean = amount > 0
    fun formattedDate(): String = date.toString()
}
@Serializable
data class Budget(val id: Long, val categoryId: Long, val amount: Double, val month: Instant) {
    fun remainingAmount(totalSpent: Double): Double = amount - totalSpent
    fun usagePercentage(totalSpent: Double): Double = if (amount <= 0) 0.0 else (totalSpent / amount).coerceIn(0.0, 1.0)
}
@Serializable
data class CategoryStats(val category: Category, val totalSpent: Double, val budget: Double?, val transactionCount: Int) {
    val budgetUsage: Double get() = if (budget != null && budget > 0) (totalSpent / budget).coerceIn(0.0, 1.0) else 0.0
}
