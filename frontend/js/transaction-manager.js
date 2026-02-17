// Transaction Manager - Handles transaction confirmations
class TransactionManager {
  constructor(appState) {
    this.appState = appState;
    this.modal = null;
  }

  init() {
    this.modal = new bootstrap.Modal(document.getElementById('transaction-modal'));
    window.addEventListener('transaction-confirmation', (e) => this.showConfirmation(e.detail));
    
    document.getElementById('transaction-confirm-btn').addEventListener('click', () => this.confirmTransaction());
    document.getElementById('transaction-cancel-btn').addEventListener('click', () => this.cancelTransaction());
    
    Logger.log('Transaction', 'Transaction manager initialized');
  }

  showConfirmation(transaction) {
    this.appState.setState({ currentTransaction: transaction });
    
    document.getElementById('transaction-type').textContent = transaction.type || 'Transferencia';
    document.getElementById('transaction-amount').textContent = `$${transaction.amount || '0.00'}`;
    document.getElementById('transaction-destination').textContent = transaction.destination || 'N/A';
    
    this.modal.show();
  }

  confirmTransaction() {
    const state = this.appState.getState();
    const transaction = state.currentTransaction;
    
    window.wsManager.send({
      action: 'confirm_transaction',
      transaction_id: transaction.id,
      user_id: state.user.id,
      session_id: state.user.sessionId
    });
    
    this.modal.hide();
    this.showToast('Transacción confirmada', 'success');
    this.appState.setState({ currentTransaction: null });
  }

  cancelTransaction() {
    this.modal.hide();
    this.showToast('Transacción cancelada', 'info');
    this.appState.setState({ currentTransaction: null });
  }

  showToast(message, type) {
    window.dispatchEvent(new CustomEvent('show-toast', { detail: { message, type } }));
  }
}

window.TransactionManager = TransactionManager;
