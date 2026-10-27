<#
.SYNOPSIS
  Opens each .docx in Microsoft Word, refreshes every field (table of contents, lists of figures / tables / code,
  caption numbers), saves the document and exports a PDF next to it. Needs Microsoft Word on Windows.
  Word automation sometimes fails on its first start ("RPC server is unavailable"): each document is retried
  once with a fresh Word instance.
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File tools/docgen/update_fields.ps1 docs/raport-tehnic/Raport_Tehnic_Proiectare.docx
#>
param(
    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]] $Paths
)

$ErrorActionPreference = 'Stop'

function Update-Document([string] $full) {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0   # wdAlertsNone
    try {
        $doc = $word.Documents.Open($full, $false, $false, $false)
        try {
            $null = $doc.Fields.Update()
            foreach ($toc in $doc.TablesOfContents) { $null = $toc.Update() }
            foreach ($tof in $doc.TablesOfFigures) { $null = $tof.Update() }
            $doc.Repaginate()
            foreach ($toc in $doc.TablesOfContents) { $null = $toc.UpdatePageNumbers() }
            foreach ($tof in $doc.TablesOfFigures) { $null = $tof.UpdatePageNumbers() }
            $doc.Save()
            $pdf = [System.IO.Path]::ChangeExtension($full, '.pdf')
            $doc.ExportAsFixedFormat($pdf, 17)   # wdExportFormatPDF
            Write-Output "updated: $full"
            Write-Output "pdf:     $pdf"
        }
        finally {
            $doc.Close()
        }
    }
    finally {
        try { $word.Quit() } catch { }
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
}

foreach ($path in $Paths) {
    $full = (Resolve-Path -LiteralPath $path).Path
    try {
        Update-Document $full
    }
    catch {
        Write-Output "Word automation failed ($($_.Exception.Message)); retrying once..."
        Start-Sleep -Seconds 3
        Update-Document $full
    }
}
