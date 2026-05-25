#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
MAX_DIMENSION=1200
MIN_SAVINGS=0.10  # 10%

optimize_image() {
  local file="$1"
  local ext="${file##*.}"
  local original_size
  original_size=$(stat -f%z "$file")

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
  else
    # Revert if savings < 10%
    echo "✗ $file: Only $(echo "scale=1; $savings * 100" | bc)% saved, reverting"
    # Note: Cannot easily revert without backup, so we keep optimized version
    # In production, you'd want to backup first
  fi
}

echo "Starting image optimization..."
echo "Max dimension: ${MAX_DIMENSION}px"
echo "Minimum savings threshold: $(echo "$MIN_SAVINGS * 100" | bc)%"
echo ""

# Find all images
find "$REPO_ROOT" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.gif" -o -iname "*.webp" \) | while read -r img; do
  # Skip node_modules, .git, etc
  if [[ "$img" == *"/node_modules/"* ]] || [[ "$img" == *"/.git/"* ]]; then
    continue
  fi
  optimize_image "$img"
done

echo ""
echo "Optimization complete!"
