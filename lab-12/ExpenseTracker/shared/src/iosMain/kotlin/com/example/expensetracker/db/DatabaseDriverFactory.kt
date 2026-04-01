package com.example.expensetracker.db
import app.cash.sqldelight.db.SqlDriver
import app.cash.sqldelight.driver.native.NativeSqliteDriver
import com.example.expensetracker.ExpenseDatabase
actual class DatabaseDriverFactory {
    actual fun createDriver(): SqlDriver = NativeSqliteDriver(ExpenseDatabase.Schema, "expense.db")
}
