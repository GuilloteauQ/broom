{
  description = "A very basic flake";

  outputs = { self, nixpkgs }: {

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.oar-of-tasks;

    packages.x86_64-linux.broom =
    with import nixpkgs { system = "x86_64-linux";};
    python37Packages.buildPythonPackage rec {
      name = "broom";
      version = "1.0";

      src = ./.;
      propagatedBuildInputs = with python37Packages; [
        pyyaml
        # collections
        # subprocess
      ];

      doCheck = false;

      # postInstall = ''
      #   cp -r app/ $out
      # '';
    };



  };
}
