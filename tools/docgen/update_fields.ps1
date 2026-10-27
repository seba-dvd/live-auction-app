<#
.SYNOPSIS
  Opens each .docx in Microsoft Word, refreshes every field (table of contents, lists of figures / tables / code,
  caption numbers), saves the document and exports a PDF next to it. Needs Microsoft Word on Windows.
.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File tools/docgen/update_fields.ps1 docs/raport-tehnic/Raport_Tehnic_Proiectare.docx
#>
param(
    [Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)]
    [string[]] $Paths
)

$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0   # wdAlertsNone
try {
    foreach ($path in $Paths) {
        $full = (Resolve-Path -LiteralPath $path).Path
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
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
