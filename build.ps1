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

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py check
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
