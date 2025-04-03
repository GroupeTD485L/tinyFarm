package com.example.tinyfarm.service;

import java.time.LocalDateTime;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.tinyfarm.entity.Vache;
import com.example.tinyfarm.entity.Ferme;
import com.example.tinyfarm.entity.Produit;
import com.example.tinyfarm.entity.Remise;
import com.example.tinyfarm.repository.VacheRepository;
import com.example.tinyfarm.repository.FermeRepository;
import com.example.tinyfarm.repository.RemiseRepository;
import com.example.tinyfarm.repository.ProduitRepository;


@Service
public class VacheService {

    private final VacheRepository vacheRepository;
    private final FermeRepository fermeRepository;
    private final RemiseRepository remiseRepository;
    private final ProduitRepository produitRepository;

    public VacheService(VacheRepository vacheRepository, FermeRepository fermeRepository, RemiseRepository remiseRepository,ProduitRepository produitRepository ){
        this.vacheRepository = vacheRepository;
        this.fermeRepository = fermeRepository;
        this.remiseRepository = remiseRepository;
        this.produitRepository = produitRepository;
    }

    @Transactional
    public Vache createCow(){
        return new Vache();
    }
    /**
     * Obtenir les informations de la vache
     */
    @Transactional
    public Vache getInfoCow(Ferme ferme) {
        return vacheRepository.findByProprietaire(ferme);
    }
    
    
    /**
     * Mettre à jour les informations de la vache en fin de journee
     */
    @Transactional
    public Vache updateVache(Ferme ferme) {
        Vache vache = ferme.getVache();
        
        if (vache == null) {
            return null;
        }

        vache.setAge(vache.getAge()+1);

        //malade depuis plus  de 4 jours donc meurt
        if (vache.getMaladeDepuis() != null 
            && vache.getMaladeDepuis().isBefore(LocalDateTime.now().minusDays(4))) {
            ferme.setVache(null);
            fermeRepository.save(ferme);
            vacheRepository.delete(vache);
            return null;
        }
        
        return vacheRepository.save(vache);
    }

    /**
     * Mettre a jour la quantite de lait de la vache (une fois a 6h et une a 18h)
     */
    @Transactional
    public Vache updateLaitVache(Ferme ferme) {
        Vache vache = ferme.getVache();
        
        //si il n'y a pas de vache
        if (vache == null) {
            return null;
        }

        //la vache peut produire du lait
        if (vache.getMaladeDepuis() == null 
            && vache.getDernierLavage().isAfter(LocalDateTime.now().minusHours(24)) 
            && vache.getDernierRepas().getDayOfMonth()==LocalDateTime.now().getDayOfMonth()){
            //la vache n'a pas ete trait
            if (vache.getQt_lait()>0){
                vache.setQt_lait(vache.getQt_lait() + 4);
                if (vache.getQt_lait() > 16){vache.setQt_lait(16);}
            }
            else {
                vache.setQt_lait(6);
            }
        }

        //elle est sale ou malade donc ne produit pas de lait
        else {
            vache.setQt_lait(0);
        }
        
        return vacheRepository.save(vache);
    }
    
    /**
     * Nourrir la vache
     */
    @Transactional
    public Vache nourrirVache(Ferme ferme, String nourriture) {
        Vache vache = ferme.getVache();
        if (vache == null) {
            return null;
        }
        if (vache.getDernierRepas() != null && 
        vache.getDernierRepas().isBefore(LocalDateTime.now().minusHours(24))) {
        if (nourriture.equals("Herbe")) {
            if (vache.getPoids()+5 <= 750){
                vache.setPoids(vache.getPoids() + 5);
                vache.setDernierRepas(LocalDateTime.now());
            }
            else if (vache.getPoids()<750 && vache.getPoids()+5 > 750 ){
                vache.setPoids(750);
                vache.setDernierRepas(LocalDateTime.now());
            }
            }
            if (nourriture.equals("Paille")) {                
                Optional<Produit> existp = produitRepository.findByNom("Paille");
                if (!existp.isPresent()) {
                    throw new IllegalArgumentException("Le produit n'existe pas");
                }
                Produit p = existp.get();
                
                Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,vache.getProprietaire());
                if (!existingRemise.isPresent()) {
                    throw new IllegalArgumentException("Produit non trouvé dans la remise");
                }
                Remise remise = existingRemise.get();

                if ( remise.getQuantite() > 0 ){
                    if (vache.getPoids()+3 <= 750) {
                        vache.setPoids(vache.getPoids() + 3);
                        vache.setDernierRepas(LocalDateTime.now());
                        remise.setQuantite(remise.getQuantite()-1);
                        remiseRepository.save(remise);
                    }
                    else if (vache.getPoids()<750 && vache.getPoids()+3 > 750) {
                        vache.setPoids(750);
                        vache.setDernierRepas(LocalDateTime.now());
                        remise.setQuantite(remise.getQuantite()-1);
                        remiseRepository.save(remise);
                    }
                }
            }
            return vacheRepository.save(vache);
        }
        return vache;
    }
    
    /**
     * Abreuver la vache
     */
    @Transactional
    public Vache abreuverVache(Ferme ferme) {
        Vache vache = ferme.getVache();
        if (vache == null) {
            return null;
        }

        Optional<Produit> existp =  produitRepository.findByNom("Seau d'eau");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();
                
        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,vache.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            vache.setDernierBreuvage(LocalDateTime.now());
            remise.setQuantite(remise.getQuantite()-1);
        }

        return vacheRepository.save(vache);
    }
    
    /**
     * Soigner la vache
     */
    @Transactional
    public Vache soignerVache(Ferme ferme) {
        Vache vache = ferme.getVache();
        if (vache == null) {
            return null;
        }
        
        // Si la vache est malade, on la soigne
        if (vache.getMaladeDepuis() != null) {
            Optional<Produit> existp =  produitRepository.findByNom("Seringue");
            if (!existp.isPresent()) {
                throw new IllegalArgumentException("Le produit n'existe pas");
            }
            Produit p = existp.get();
            
            Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,vache.getProprietaire());
            if (!existingRemise.isPresent()) {
                throw new IllegalArgumentException("Produit non trouvé dans la remise");
            }
            Remise remise = existingRemise.get();
            if (remise.getQuantite()>0 ){
                remise.setQuantite(remise.getQuantite()-1);
                vache.setMaladeDepuis(null);
            }
            
            return vacheRepository.save(vache);
        }

        return(vache);
    }
    
    /**
     * Laver la vache
     */
    @Transactional
    public Vache laverVache(Ferme ferme) {
        Vache vache = ferme.getVache();
        if (vache == null) {
            return null;
        }

        Optional<Produit> existp =  produitRepository.findByNom("Savon");
        if (!existp.isPresent()) {
            throw new IllegalArgumentException("Le produit n'existe pas");
        }
        Produit p = existp.get();

        Optional<Remise> existingRemise = remiseRepository.findByIdProduitAndProprietaire(p,vache.getProprietaire());
        if (!existingRemise.isPresent()) {
            throw new IllegalArgumentException("Produit non trouvé dans la remise");
        }
        Remise remise = existingRemise.get();
        if (remise.getQuantite()>0 ){
            remise.setQuantite(remise.getQuantite()-1);
            vache.setDernierLavage(LocalDateTime.now());
        }
                
        return vacheRepository.save(vache);
    }

    @Transactional
    public Vache faireMalade(Ferme ferme) {
        Vache vache = ferme.getVache();
        if (vache == null) {
            return null;
        }
        vache.setMaladeDepuis(LocalDateTime.now().minusDays(4));
        return vacheRepository.save(vache);
    }
    
}


/*  
GET         /comptes/{id}/fermes/{id}/vache  Obtenir les infos de la vache
PUT         /comptes/{id}/fermes/{id}/vache  Update les infos de la vache
PUT         /vache/nourrir Nourrir la vache
PUT         /vache/abreuver Abreuver la vache
PUT         /vache/soigner Soigner la vache
PUT         /vache/laver Laver la vache
 */