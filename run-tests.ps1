#!/usr/bin/env powershell
<#
.SYNOPSIS
Interactive test runner for RoadWatch MVP
.DESCRIPTION
Provides menu-driven testing of all services
#>

param(
    [switch]$SkipMenu = $false
)

$ErrorActionPreference = "Continue"

# Helper functions
function Show-Banner {
    @"
╔════════════════════════════════════════════════════════════════════╗
║          RoadWatch MVP - Interactive Test Runner                  ║
╚════════════════════════════════════════════════════════════════════╝
"@ | Write-Host -ForegroundColor Cyan
}

function Test-Service {
    param([string]$Name, [string]$Url)
    
    try {
        $result = Invoke-WebRequest -Uri $Url -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($result.StatusCode -eq 200) {
            Write-Host "[OK]" -ForegroundColor Green -NoNewline
            Write-Host " $Name is responding"
            return $true
        }
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " $Name is not responding"
        return $false
    }
}

function Test-CitizenSignup {
    Write-Host "`n[TEST] Citizen Signup..." -ForegroundColor Yellow
    
    $body = @{
        email = "testcitizen@example.com"
        full_name = "Test Citizen"
        citizen_id = "TEST_CITIZEN_$(Get-Random)"
        password = "TestPass123!"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/auth/signup" `
          -Method Post `
          -Headers @{"Content-Type"="application/json"} `
          -Body $body `
          -ErrorAction SilentlyContinue
        
        $data = $response.Content | ConvertFrom-Json
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Citizen signup successful: $($data.citizen_id)"
        return $data.citizen_id, $body | ConvertFrom-Json | Select-Object -ExpandProperty password
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " Citizen signup failed: $($_.Exception.Message)"
        return $null, $null
    }
}

function Test-CitizenLogin {
    param([string]$CitizenId, [string]$Password)
    
    Write-Host "`n[TEST] Citizen Login..." -ForegroundColor Yellow
    
    $body = @{
        citizen_id = $CitizenId
        password = $Password
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/auth/login" `
          -Method Post `
          -Headers @{"Content-Type"="application/json"} `
          -Body $body `
          -ErrorAction SilentlyContinue
        
        $data = $response.Content | ConvertFrom-Json
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Citizen login successful"
        return $data.token
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " Citizen login failed"
        return $null
    }
}

function Test-SubmitReport {
    param([string]$Token, [string]$CitizenId)
    
    Write-Host "`n[TEST] Submit Report..." -ForegroundColor Yellow
    
    $body = @{
        violation_type = "helmet"
        description = "Test violation - rider without helmet"
        location = "Test Street, City"
        vehicle_number = "TEST123"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/reports" `
          -Method Post `
          -Headers @{
              "Authorization" = "Bearer $Token"
              "Content-Type" = "application/json"
          } `
          -Body $body `
          -ErrorAction SilentlyContinue
        
        $data = $response.Content | ConvertFrom-Json
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Report submitted: $($data.report_id)"
        return $data.report_id
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " Report submission failed"
        return $null
    }
}

function Test-OfficerFlow {
    Write-Host "`n[TEST] Officer Registration..." -ForegroundColor Yellow
    
    $body = @{
        officer_id = "TEST_OFFICER_$(Get-Random)"
        full_name = "Test Officer"
        station = "Test Station"
        password = "TestPass123!"
    } | ConvertTo-Json
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/officer/register" `
          -Method Post `
          -Headers @{"Content-Type"="application/json"} `
          -Body $body `
          -ErrorAction SilentlyContinue
        
        $regData = $response.Content | ConvertFrom-Json
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Officer registered: $($regData.officer_id)"
        
        # Login
        Write-Host "`n[TEST] Officer Login..." -ForegroundColor Yellow
        $loginBody = @{
            officer_id = $regData.officer_id
            password = "TestPass123!"
        } | ConvertTo-Json
        
        $loginResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/officer/login" `
          -Method Post `
          -Headers @{"Content-Type"="application/json"} `
          -Body $loginBody `
          -ErrorAction SilentlyContinue
        
        $loginData = $loginResponse.Content | ConvertFrom-Json
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Officer login successful"
        
        return $loginData.token
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " Officer flow failed"
        return $null
    }
}

function Test-ReportQueue {
    param([string]$OfficerToken)
    
    Write-Host "`n[TEST] View Report Queue..." -ForegroundColor Yellow
    
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/authority/reports" `
          -Headers @{"Authorization" = "Bearer $OfficerToken"} `
          -ErrorAction SilentlyContinue
        
        $data = $response.Content | ConvertFrom-Json
        
        if ($data -is [array]) {
            $count = $data.Count
        } else {
            $count = if ($data) { 1 } else { 0 }
        }
        
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Found $count reports in queue"
        
        return $data
    }
    catch {
        Write-Host "[FAIL]" -ForegroundColor Red -NoNewline
        Write-Host " Could not retrieve report queue"
        return $null
    }
}

function Show-Menu {
    @"

Select test to run:
  [1] Verify all services are up
  [2] Test citizen signup & login
  [3] Test report submission
  [4] Test officer flow
  [5] Run full end-to-end test
  [6] Check API documentation
  [7] View service logs
  [8] Exit

"@ | Write-Host -ForegroundColor Cyan
}

# Main
Show-Banner

Write-Host "`nServices Status:`n" -ForegroundColor Cyan

$backendUp = Test-Service "Backend API" "http://127.0.0.1:8001/health"
$gatewayUp = Test-Service "AI Gateway" "http://127.0.0.1:9999/openapi.json"

if (-not ($backendUp -and $gatewayUp)) {
    Write-Host "`n[WARNING] Some services are not responding!" -ForegroundColor Yellow
    Write-Host "Start them with: & '.\start-services.ps1'" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[SUCCESS] All core services are running!`n" -ForegroundColor Green

while ($true) {
    Show-Menu
    $choice = Read-Host "Enter choice (1-8)"
    
    switch ($choice) {
        "1" {
            Write-Host "`n[INFO] Testing all services...`n" -ForegroundColor Cyan
            Test-Service "Backend API" "http://127.0.0.1:8001/health" | Out-Null
            Test-Service "AI Gateway" "http://127.0.0.1:9999/openapi.json" | Out-Null
        }
        
        "2" {
            $citizenId, $password = Test-CitizenSignup
            if ($citizenId) {
                $token = Test-CitizenLogin $citizenId $password
                if ($token) {
                    Write-Host "`n[INFO] Citizen credentials saved for next test" -ForegroundColor Green
                }
            }
        }
        
        "3" {
            Write-Host "`n[INFO] Running citizen signup + report submission..." -ForegroundColor Cyan
            $citizenId, $password = Test-CitizenSignup
            if ($citizenId) {
                $token = Test-CitizenLogin $citizenId $password
                if ($token) {
                    $reportId = Test-SubmitReport $token $citizenId
                    if ($reportId) {
                        Write-Host "`n[INFO] Report created for officer review" -ForegroundColor Green
                    }
                }
            }
        }
        
        "4" {
            Write-Host "`n[INFO] Running officer flow..." -ForegroundColor Cyan
            $officerToken = Test-OfficerFlow
            if ($officerToken) {
                $queue = Test-ReportQueue $officerToken
            }
        }
        
        "5" {
            Write-Host "`n[INFO] Running full end-to-end test..." -ForegroundColor Cyan
            
            # Citizen flow
            $citizenId, $password = Test-CitizenSignup
            if ($citizenId) {
                $citizenToken = Test-CitizenLogin $citizenId $password
                if ($citizenToken) {
                    $reportId = Test-SubmitReport $citizenToken $citizenId
                    
                    # Officer flow
                    if ($reportId) {
                        $officerToken = Test-OfficerFlow
                        if ($officerToken) {
                            $queue = Test-ReportQueue $officerToken
                            Write-Host "`n[SUCCESS] Full end-to-end test completed!" -ForegroundColor Green
                        }
                    }
                }
            }
        }
        
        "6" {
            Write-Host "`n[INFO] Opening API documentation..." -ForegroundColor Cyan
            Start-Process "http://127.0.0.1:8001/api/docs"
            Write-Host "[INFO] Browser opened to http://127.0.0.1:8001/api/docs`n" -ForegroundColor Green
        }
        
        "7" {
            Write-Host "`n[INFO] View logs in the service terminal windows:" -ForegroundColor Cyan
            Write-Host "  Terminal 1: AI Gateway logs" -ForegroundColor Gray
            Write-Host "  Terminal 2: Backend API logs" -ForegroundColor Gray
            Write-Host "  Terminal 3: Frontend logs`n" -ForegroundColor Gray
        }
        
        "8" {
            Write-Host "`nGoodbye!`n" -ForegroundColor Cyan
            exit 0
        }
        
        default {
            Write-Host "[ERROR] Invalid choice. Please select 1-8.`n" -ForegroundColor Red
        }
    }
}
