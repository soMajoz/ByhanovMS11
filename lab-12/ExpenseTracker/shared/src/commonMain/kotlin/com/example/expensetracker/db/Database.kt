package com.example.expensetracker.db
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.coroutines.*
import com.example.expensetracker.ExpenseDatabase
import com.example.expensetracker.models.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.IO
import kotlinx.coroutines.flow.*
import kotlinx.datetime.*
class Database(driver: SqlDriver) {
    private val db = ExpenseDatabase(driver)
    fun getAllCategories(): Flow<List<Category>> = db.categoryQueries.selectAll().asFlow().mapToList(Dispatchers.IO).map { list ->
        list.map { Category(it.id, it.name, it.color, it.icon, it.isDefault == 1L) }
    }
    suspend fun insertExpense(e: Expense) = db.expenseQueries.insert(e.amount, e.categoryId, e.description, e.date.toEpochMilliseconds(), if (e.isSynced) 1 else 0)
    fun getExpensesForMonth(y: Int, m: Int): Flow<List<Expense>> {
        val start = LocalDate(y, m, 1).atStartOfDayIn(TimeZone.currentSystemDefault()).toEpochMilliseconds()
        val end = LocalDate(y, m, 1).plus(1, DateTimeUnit.MONTH).atStartOfDayIn(TimeZone.currentSystemDefault()).toEpochMilliseconds()
        return db.expenseQueries.selectByDateRange(start, end).asFlow().mapToList(Dispatchers.IO).map { list ->
            list.map { Expense(it.id, it.amount, it.categoryId, it.description, Instant.fromEpochMilliseconds(it.date), it.isSynced == 1L) }
        }
    }
    suspend fun deleteExpense(id: Long) = db.expenseQueries.deleteById(id)
    suspend fun getCategoryStats(y: Int, m: Int): Flow<List<CategoryStats>> = combine(getAllCategories(), getExpensesForMonth(y, m), getBudgetForMonth(y, m)) { cats, exps, buds ->
        cats.map { cat ->
            val spent = exps.filter { it.categoryId == cat.id }.sumOf { it.amount }
            val bud = buds.find { it.categoryId == cat.id }?.amount
            val count = exps.count { it.categoryId == cat.id }
            CategoryStats(cat, spent, bud, count)
        }
    }
    fun getBudgetForMonth(y: Int, m: Int): Flow<List<Budget>> {
        val monthStart = LocalDate(y, m, 1).atStartOfDayIn(TimeZone.currentSystemDefault()).toEpochMilliseconds()
        return db.budgetQueries.selectByMonth(monthStart).asFlow().mapToList(Dispatchers.IO).map { list ->
            list.map { Budget(it.id, it.categoryId, it.amount, Instant.fromEpochMilliseconds(it.month)) }
        }
    }
}
