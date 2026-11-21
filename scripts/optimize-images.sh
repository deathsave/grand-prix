#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
MAX_DIMENSION=1200
MIN_SAVINGS=0.10  # 10%
MANIFEST="$REPO_ROOT/.optimize-images-manifest"

# Manifest entries are "path|size" lines. Updates are
# appended to a working copy (last entry for a path wins)
# so this runs on macOS's bash 3.2 (no associative arrays).
MANIFEST_WORK="${MANIFEST}.tmp"
if [ -f "$MANIFEST" ]; then
  cp "$MANIFEST" "$MANIFEST_WORK"
else
  : > "$MANIFEST_WORK"
fi

manifest_get() {
  awk -F'|' -v p="$1" '$1 == p { v = $2 } END { print v }' "$MANIFEST_WORK"
}

manifest_set() {
  echo "${1}|${2}" >> "$MANIFEST_WORK"
}

# Save manifest, keeping only the latest entry per path
save_manifest() {
  awk -F'|' '{ v[$1] = $2 } END { for (p in v) print p "|" v[p] }' \
    "$MANIFEST_WORK" | sort > "$MANIFEST"
  rm -f "$MANIFEST_WORK"
}

optimize_image() {
  local file="$1"
  local current_size
  current_size=$(stat -f%z "$file")

  # Skip if already optimized (size matches manifest)
  if [ "$(manifest_get "$file")" = "$current_size" ]; then
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
    manifest_set "$file" "$new_size"
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
  # Skip node_modules, .git, misc, etc
  if [[ "$img" == *"/node_modules/"* ]] || [[ "$img" == *"/.git/"* ]] ||
     [[ "$img" == "$REPO_ROOT/misc/"* ]]; then
    continue
  fi
  optimize_image "$img"
done < <(find "$REPO_ROOT" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \))

echo ""
echo "Optimization complete!"
save_manifest
echo "Manifest saved to $MANIFEST"
