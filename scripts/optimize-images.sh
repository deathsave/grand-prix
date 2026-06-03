#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
MAX_DIMENSION=1200
MIN_SAVINGS=0.10  # 10%
MANIFEST="$REPO_ROOT/.optimize-images-manifest"

# Load existing manifest
declare -A MANIFEST_ENTRIES
if [ -f "$MANIFEST" ]; then
  while IFS='|' read -r path size; do
    MANIFEST_ENTRIES["$path"]="$size"
  done < "$MANIFEST"
fi

# Save manifest
save_manifest() {
  local tmp="${MANIFEST}.tmp"
  > "$tmp"
  for path in "${!MANIFEST_ENTRIES[@]}"; do
    echo "${path}|${MANIFEST_ENTRIES[$path]}" >> "$tmp"
  done
  mv "$tmp" "$MANIFEST"
}

optimize_image() {
  local file="$1"
  local current_size
  current_size=$(stat -f%z "$file")

  # Skip if already optimized (size matches manifest)
  if [ "${MANIFEST_ENTRIES[$file]:-}" = "$current_size" ]; then
    echo "⏭ $file: already optimized, skipping"
    return
  fi

  local ext="${file##*.}"
  local original_size="$current_size"
  local backup="${file}.optimize-backup"

  # Backup original
  cp "$file" "$backup"

  # Get current dimensions
  local width height
  width=$(identify -format "%w" "$file" 2>/dev/null)
  height=$(identify -format "%h" "$file" 2>/dev/null)

  # Resize if larger than MAX_DIMENSION
  if [ "$width" -gt "$MAX_DIMENSION" ] || [ "$height" -gt "$MAX_DIMENSION" ]; then
    echo "Resizing $file (${width}x${height} -> max ${MAX_DIMENSION}px)"
    convert "$file" -resize "${MAX_DIMENSION}x${MAX_DIMENSION}>" "$file"
  fi

  # Optimize based on file type
  case "$ext" in
    png)
      pngquant --quality=65-80 --force --output "$file" "$file" 2>/dev/null || true
      optipng -o7 -quiet "$file" 2>/dev/null || true
      ;;
    jpg|jpeg)
      jpegoptim --max=85 --strip-all --quiet "$file" 2>/dev/null || true
      ;;
    webp)
      cwebp -q 80 "$file" -o "${file}.tmp" 2>/dev/null && mv "${file}.tmp" "$file" || true
      ;;
  esac

  # Check savings
  local new_size
  new_size=$(stat -f%z "$file")
  local savings
  savings=$(echo "scale=4; ($original_size - $new_size) / $original_size" | bc)

  if (( $(echo "$savings >= $MIN_SAVINGS" | bc -l) )); then
    local savings_pct
    savings_pct=$(echo "scale=1; $savings * 100" | bc)
    echo "✓ $file: ${original_size} -> ${new_size} bytes (${savings_pct}% saved)"
    MANIFEST_ENTRIES["$file"]="$new_size"
    rm -f "$backup"
  else
    # Revert if savings < 10%
    echo "✗ $file: Only $(echo "scale=1; $savings * 100" | bc)% saved, reverting"
    mv "$backup" "$file"
  fi
}

echo "Starting image optimization..."
echo "Max dimension: ${MAX_DIMENSION}px"
echo "Minimum savings threshold: $(echo "$MIN_SAVINGS * 100" | bc)%"
echo ""

# Find all images
while read -r img; do
  # Skip node_modules, .git, etc
  if [[ "$img" == *"/node_modules/"* ]] || [[ "$img" == *"/.git/"* ]]; then
    continue
  fi
  optimize_image "$img"
done < <(find "$REPO_ROOT" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \))

echo ""
echo "Optimization complete!"
save_manifest
echo "Manifest saved to $MANIFEST"
