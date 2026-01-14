from rich.console import Console

# Initialize a rich console for styled output
console = Console()

def log_info(message):
    """Logs general information messages."""
    console.print(f"[bold cyan]INFO:[/bold cyan] {message}")

def log_success(message):
    """Logs successful outcomes."""
    console.print(f"[bold green]SUCCESS:[/bold green] {message}")

def log_warning(message):
    """Logs potential issues or non-critical results."""
    console.print(f"[bold yellow]WARN:[/bold yellow] {message}")

def log_error(message):
    """Logs critical errors."""
    console.print(f"[bold red]ERROR:[/bold red] {message}")