#!/bin/bash
# Test PyDEA across multiple Python versions using uv
#
# Usage:
#   bash test_all_versions.sh          # Test all versions
#   bash test_all_versions.sh 3.12     # Test specific version only

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Supported Python versions
VERSIONS=("3.8" "3.9" "3.10" "3.11" "3.12" "3.13")

# If a specific version is provided, test only that version
if [ ! -z "$1" ]; then
    VERSIONS=("$1")
fi

echo "==========================================="
echo "Testing PyDEA with multiple Python versions"
echo "==========================================="
echo ""

FAILED_VERSIONS=()
PASSED_COUNT=0
FAILED_COUNT=0

for version in "${VERSIONS[@]}"; do
    echo -e "${BLUE}Testing Python ${version}...${NC}"

    if uv run --python $version pytest tests/ -q --tb=short 2>&1; then
        echo -e "${GREEN}✅ Python ${version}: PASSED${NC}"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    else
        echo -e "${RED}❌ Python ${version}: FAILED${NC}"
        FAILED_VERSIONS+=($version)
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
    echo ""
done

echo "==========================================="
echo "Test Summary"
echo "==========================================="
echo -e "${GREEN}Passed: ${PASSED_COUNT}${NC}"
echo -e "${RED}Failed: ${FAILED_COUNT}${NC}"

if [ ${#FAILED_VERSIONS[@]} -gt 0 ]; then
    echo ""
    echo -e "${RED}Failed versions: ${FAILED_VERSIONS[*]}${NC}"
    exit 1
else
    echo ""
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
fi
