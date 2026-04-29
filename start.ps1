$ErrorActionPreference = "Stop"

if (Test-Path ".\.env") {
    Get-Content ".\.env" | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#") -and $line.Contains("=")) {
            $name, $value = $line.Split("=", 2)
            [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
        }
    }
}

$port = if ($env:WAITRESS_PORT) { $env:WAITRESS_PORT } else { "8000" }
$threads = if ($env:WAITRESS_THREADS) { $env:WAITRESS_THREADS } else { "4" }

python manage.py migrate --noinput
python manage.py create_admin_if_missing

waitress-serve --listen="0.0.0.0:$port" --threads=$threads plit99_project.wsgi:application
