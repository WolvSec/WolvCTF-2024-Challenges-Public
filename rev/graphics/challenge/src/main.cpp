#include <RavEngine/App.hpp>
#include <RavEngine/StaticMesh.hpp>
#include <RavEngine/World.hpp>
#include <RavEngine/CameraComponent.hpp>
#include <RavEngine/GameObject.hpp>
#include <RavEngine/Dialogs.hpp>
#include <RavEngine/GUI.hpp>
#include <RavEngine/StartApp.hpp>
#include <RavEngine/InputManager.hpp>
#include <RavEngine/AnimatorComponent.hpp>
#include <RavEngine/MeshAssetSkinned.hpp>
#include <RavEngine/SkinnedMeshComponent.hpp>
#include <RavEngine/SkeletonAsset.hpp>
#include "flag.h"
#include "obfuscate.h"

using namespace RavEngine;
using namespace std;

struct CTFWorld : public RavEngine::World {

    ComponentHandle<Transform> rootTransform;

	CTFWorld() {
		auto cameraEntity = CreatePrototype<GameObject>();
        auto& cameraComponent = cameraEntity.EmplaceComponent<CameraComponent>();
		cameraComponent.SetActive(true);
        cameraEntity.GetTransform().LocalTranslateDelta({0,1,4});

		auto lightsEntity = CreatePrototype<GameObject>();
		lightsEntity.EmplaceComponent<DirectionalLight>().SetIntensity(4);
		lightsEntity.EmplaceComponent<AmbientLight>().SetIntensity(0.2);

		lightsEntity.GetTransform().LocalRotateDelta(vector3{ deg_to_rad(45), deg_to_rad(45),0 });
        
        //setup the UI
        auto guiEntity = CreatePrototype<GameObject>();
        auto& gui = guiEntity.EmplaceComponent<GUIComponent>();
        auto doc = gui.AddDocument("ui.rml");
        
        auto bodyelt = doc->GetElementById("body");

        auto setSharedProperties = [](auto&& elt) {
            elt->SetProperty("width","100%");
            elt->SetProperty("position","absolute");
            elt->SetProperty("top","30dp");
            elt->SetProperty("left","0dp");
            elt->SetProperty("white-space","nowrap");
        };
        
        auto flagElt = doc->CreateElement("p");

        std::string dec_flag(AY_OBFUSCATE(FLAG));

        flagElt->SetInnerRML(dec_flag);
        setSharedProperties(flagElt);
        bodyelt->AppendChild(std::move(flagElt));
        
        auto coverElt = doc->CreateElement("p");
        coverElt->SetInnerRML("ooh spinny");
        setSharedProperties(coverElt);
        coverElt->SetProperty("background-color","#FF00FFFF");
        bodyelt->AppendChild(std::move(coverElt));
        
        //gui.Debug();
        
        //input manager
        Ref<InputManager> im = RavEngine::New<InputManager>();
        im->AddAxisMap("MouseX", Special::MOUSEMOVE_X);
        im->AddAxisMap("MouseY", Special::MOUSEMOVE_Y);
        
        ComponentHandle<GUIComponent> g(guiEntity);
        im->BindAxis("MouseX", g, &GUIComponent::MouseX, CID::ANY,0);
        im->BindAxis("MouseY", g, &GUIComponent::MouseY, CID::ANY,0);
        im->BindAnyAction(g->GetData());
        
        GetApp()->inputManager = im;

        // decorations

        auto rootObj = CreatePrototype<GameObject>();

        // flagpole
        auto flagMat = RavEngine::New<PBRMaterialInstance>(Material::Manager::Get<PBRMaterial>());
        flagMat->SetAlbedoColor({1,193/255.0,0,1});

        auto baseMat = RavEngine::New<PBRMaterialInstance>(Material::Manager::Get<PBRMaterial>());;
        baseMat->SetAlbedoColor({0,32/255.0,97/255.0,1});
            
        auto flagBaseObj = CreatePrototype<GameObject>();

        auto poleMesh = MeshAsset::Manager::Get("cylinder.obj");
        auto flagPole = CreatePrototype<GameObject>();
        flagPole.EmplaceComponent<StaticMesh>(poleMesh, LitMeshMaterialInstance(flagMat));
        flagPole.GetTransform().SetLocalScale({ 0.1,1,0.1 }).LocalTranslateDelta({0,1,0});
        flagBaseObj.GetTransform().AddChild(flagPole);

        // flag top
        auto flagTopObj = CreatePrototype<GameObject>();
        flagTopObj.EmplaceComponent<StaticMesh>(MeshAsset::Manager::Get("sphere.obj"), LitMeshMaterialInstance(flagMat));
        flagTopObj.GetTransform().LocalTranslateDelta({ 0,2,0 }).SetLocalScale(0.1);
        flagBaseObj.GetTransform().AddChild(flagTopObj);

        // flag base
        auto flagStandObj = CreatePrototype<GameObject>();
        flagStandObj.EmplaceComponent<StaticMesh>(poleMesh, LitMeshMaterialInstance(baseMat));
        flagStandObj.GetTransform().SetLocalScale({1,0.1,1});
        flagBaseObj.GetTransform().AddChild(flagStandObj);

        // flag
        auto skeleton = RavEngine::New<SkeletonAsset>("flag.fbx");
        auto clips = RavEngine::New<AnimationAsset>("flag.fbx", skeleton);
        auto swingAnim = RavEngine::New<AnimationAssetSegment>(clips, 0, 59);
        auto meshAssetSkinned = MeshAssetSkinned::Manager::Get("flag.fbx", skeleton);
        auto flagEntity = CreatePrototype<GameObject>();
        flagEntity.EmplaceComponent<SkinnedMeshComponent>(skeleton, meshAssetSkinned).SetMaterial(LitMeshMaterialInstance(flagMat));
        flagEntity.GetTransform().LocalTranslateDelta({0,1.3,0});
        flagBaseObj.GetTransform().AddChild(flagEntity);

        auto& animcomp = flagEntity.EmplaceComponent<AnimatorComponent>(skeleton);

        AnimatorComponent::State all_anim{ 0, swingAnim };
        all_anim.isLooping = true;
        animcomp.InsertState(all_anim);
        animcomp.Goto(0, true);
        animcomp.Play();
        animcomp.debugEnabled = true;

        rootObj.GetTransform().AddChild(flagBaseObj);
        flagBaseObj.GetTransform().LocalRotateDelta(vector3{0,0,deg_to_rad(10)});
        rootTransform = { rootObj };
	}

	void PostTick(float tickrateScale) final {
        auto time = GetApp()->GetCurrentTime();
        rootTransform->SetWorldRotation(vector3{0,deg_to_rad(std::sin(time * 2) * 80),0});
	}
};

struct CTFGame : public RavEngine::App {

	void OnStartup(int argc, char** argv) final {
		SetWindowTitle("The flag is somewhere inside me...");

		AddWorld(RavEngine::New<CTFWorld>());
	}

	void OnFatal(const std::string_view msg) final {
		RavEngine::Dialog::ShowBasic("Fatal Error", msg, Dialog::MessageBoxType::Error);
	}
};

START_APP(CTFGame)
