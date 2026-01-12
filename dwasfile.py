from dwas import managed_step, StepRunner


@managed_step(
    ["-rrequirements.txt", "ansible-lint"],
    name="ansible-lint",
)
def ansible_lint(step: StepRunner) -> None:
    env = {
        "ANSIBLE_HOME": step.cache_path / "ansible",
        "HOME": str(step.cache_path / "home"),
    }

    step.run(
        [
            "ansible-galaxy",
            "install",
            "--role-file=extensions/molecule/default/requirements.yml",
            "--force",
        ],
        env=env,
    )

    command = ["ansible-lint", "--strict", "--offline"]
    if step.config.colors:
        command.append("--force-color")

    step.run(command, env=env)
