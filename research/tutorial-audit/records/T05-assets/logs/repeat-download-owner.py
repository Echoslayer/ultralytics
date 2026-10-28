def attempt_download_asset(
    file: str | Path,
    repo: str = "ultralytics/assets",
    release: str = "v8.4.0",
    **kwargs,
) -> str:
    """Attempt to download a file from GitHub release assets if it is not found locally.

    Args:
        file (str | Path): The filename or file path to be downloaded, or an HTTP(S) URL (scheme in any letter case) to
            download directly.
        repo (str, optional): The GitHub repository in the format 'owner/repo'.
        release (str, optional): The specific release version to be downloaded.
        **kwargs (Any): Additional keyword arguments passed to `safe_download`.

    Returns:
        (str): The path to the local or downloaded file.

    Examples:
        >>> file_path = attempt_download_asset("yolo26n.pt", repo="ultralytics/assets")
    """
    from ultralytics.utils import SETTINGS  # scoped for circular import

    # YOLOv3/5u updates
    file = Path(checks.check_yolov5u_filename(str(file).strip().replace("'", "")))
    if file.exists():
        return str(file)
    elif (SETTINGS["weights_dir"] / file).exists():
        return str(SETTINGS["weights_dir"] / file)
    else:
        # URL specified
        name = Path(parse.unquote(str(file))).name  # decode '%2F' to '/' etc.
        download_url = f"https://github.com/{repo}/releases/download"
        if str(file).lower().startswith(("http:/", "https:/")):  # download
            url = str(file).replace(":/", "://")  # Pathlib turns :// -> :/
            file = url2file(name)  # parse authentication query strings
            if Path(file).is_file():
                LOGGER.info(f"Found {clean_url(url)} locally at {file}")  # file already exists
            else:
                safe_download(url=url, file=file, min_bytes=1e5, **kwargs)

        elif repo == GITHUB_ASSETS_REPO and name in GITHUB_ASSETS_NAMES:
            safe_download(url=f"{download_url}/{release}/{name}", file=file, min_bytes=1e5, **kwargs)

        else:
            tag, assets = get_github_assets(repo, release)
            if not assets:
                tag, assets = get_github_assets(repo)  # latest release
            if name in assets:
                safe_download(url=f"{download_url}/{tag}/{name}", file=file, min_bytes=1e5, **kwargs)

        return str(file)
