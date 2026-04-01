package com.example.expensetracker.viewmodels
import com.example.expensetracker.db.Database
import com.example.expensetracker.models.*
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import kotlinx.datetime.*
class ExpensesViewModel(private val database: Database) {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)
    private val _state = MutableStateFlow(ExpensesState())
    val state: StateFlow<ExpensesState> = _state.asStateFlow()
    private val _currentMonth = MutableStateFlow(LocalDate(Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault()).year, Clock.System.now().toLocalDateTime(TimeZone.currentSystemDefault()).monthNumber, 1))
    init { loadData() }
    private fun loadData() {
        _currentMonth.flatMapLatest { date ->
            combine(database.getAllCategories(), database.getExpensesForMonth(date.year, date.monthNumber), database.getBudgetForMonth(date.year, date.monthNumber)) { cats, exps, buds ->
                ExpensesState(cats, exps, buds, false)
            }
        }.onEach { newState -> _state.value = newState }.launchIn(scope)
    }
    fun addExpense(amount: Double, categoryId: Long, description: String?) {
        scope.launch { database.insertExpense(Expense(0, amount, categoryId, description, Clock.System.now())) }
    }
    fun deleteExpense(id: Long) { scope.launch { database.deleteExpense(id) } }
}
data class ExpensesState(val categories: List<Category> = emptyList(), val expenses: List<Expense> = emptyList(), val budgets: List<Budget> = emptyList(), val isLoading: Boolean = true) {
    val totalExpenses: Double get() = expenses.sumOf { it.amount }
    val topCategories: List<Pair<Category, Double>> get() = categories.map { cat -> cat to expenses.filter { it.categoryId == cat.id }.sumOf { it.amount } }.sortedByDescending { it.second }.take(5)
}
