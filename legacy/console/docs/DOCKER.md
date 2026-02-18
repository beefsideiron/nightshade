# SunPredict Docker Documentation

## Quick Start

### Build the image
```bash
docker build -t sunpredict .
```

Or using compose:
```bash
docker-compose build
```

### Run the prediction CLI
```bash
# Using docker directly
docker run --rm sunpredict 35.1264 -106.6055 1600

# Using docker-compose
docker-compose run --rm sunpredict 35.1264 -106.6055 1600
```

### Run with terrain obstruction
```bash
docker-compose run --rm sunpredict 35.1264 -106.6055 1600 --terrain data/sample_terrain.json
```

### Run validation tests
```bash
docker-compose run --rm sunpredict python tests/validate.py
```

### Run unit tests
```bash
docker-compose run --rm sunpredict python -m pytest tests/
```

## Container Structure

- **Volumes:**
  - `./data` → `/app/data` (terrain profiles and test data)
  - `./results` → `/app/results` (output directory for predictions)

- **Working directory:** `/app`

## Notes

- All coordinates are in decimal degrees (latitude, longitude)
- Elevation is in meters above sea level
- Times are output in UTC
- Optional `--date YYYY-MM-DD` flag to specify a date (defaults to today)
