# input is *.raw, output is sld format labels.fact
cat $1 | sed '/^Author/d' | sed '/^Has/d' | sed '/^Title/d' | sed '/^Venue/d' | sed 's/.*,//g' | sed 's/)$//g' | sort -u | sed '/^ *$/d' | tr '[:upper:]' '[:lower:]' | sed 's/^/isLabel(/' | sed 's/$/)/'