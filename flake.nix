{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      pyopencv4 = pkgs.python311Packages.opencv4.override {
        enableGtk2 = true;
        gtk2 = pkgs.gtk2;
        #enableFfmpeg = true; #here is how to add ffmpeg and other compilation flags
        #ffmpeg_3 = pkgs.ffmpeg;
        };

    in
      {
        devShells.${system}.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            nodejs_20
            python311
            python311Packages.pandas
            python311Packages.numpy
            python311Packages.pyaudio
           # python311Packages.opencv4
           pyopencv4
            #python311Packages.opencv4
            gcc
          ];

          # Optional: set up environment variables or other shell hooks
          shellHook = ''
            echo "Welcome to your non-FHS development shell!"
            export OPENCV_DATA_PATH="${pkgs.opencv}/share/opencv4/haarcascades/data/"
            mkdir -p haarcascades
            ln -sf ${pkgs.opencv}/share/opencv4/haarcascades/ haarcascades/data
            export OPENCV_DATA_PATH="`pwd`/haarcascades/data"
          '';
        };
      };
}

